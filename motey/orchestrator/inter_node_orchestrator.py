import threading

import yaml
from jsonschema import validate, ValidationError

from motey.communication.api_routes.service import Service as ServiceEndpoint
from motey.models.schemas import blueprint_yaml_schema
from motey.models.service import Service
from motey.utils.network_utils import get_own_ip


class InterNodeOrchestrator(object):
    """
    This class orchestpassrates yaml blueprints.
    It will start and stop virtual instances of images defined in the blueprint.
    It also can communicate with other nodes to start instances there if the requirements does not fit with the
    possibilities of the current node.
    """
    def __init__(self, logger, valmanager, service_repository, labeling_repository, node_repository, zeromq_server):
        """
        Instantiates the ``Logger``, the ``VALManagger``, ``ServiceRepository`` and subscribe to the blueprint endpoint.
        """
        self.logger = logger
        self.valmanager = valmanager
        self.service_repository = service_repository
        self.labeling_repository = labeling_repository
        self.node_repository = node_repository
        self.zeromq_server = zeromq_server
        self.blueprint_stream = ServiceEndpoint.yaml_post_stream.subscribe(self.handle_blueprint)

    def parse_local_blueprint_file(self, file_path):
        """
        Parse a local yaml file and start the virtual images defined in the blueprint.

        :param file_path: Path to the local blueprint file.
        """
        with open(file_path, 'r') as stream:
            self.handle_blueprint(stream)

    def instantiate_service(self, service):
        """
        Instantiate a service.

        :param service: the service to be used.
        """
        if service.action == Service.ServiceAction.ADD:
            self.service_repository.add(dict(service))
            service.state = Service.ServiceState.INSTANTIATING
            self.service_repository.update(dict(service))
            for image in service.images:
                if not image.capabilities:
                    # no capabilities, deploy locally
                    image.node = get_own_ip()
                    continue

                for capability in image.capabilities:
                    if not self.labeling_repository.has(label=capability):
                        # if a single capability is not satisfied, search for external node
                        node = self.find_node(image)
                        if node:
                            image.node = node['ip']
                            # found a node which handle the container - we can break the loop
                            break
                        else:
                            # does not found any node - error
                            service.state = Service.ServiceState.ERROR
                            break
                else:
                    # never broke - all capabilities are succeeded locally
                    image.node = get_own_ip()

                if service.state == Service.ServiceState.ERROR:
                    self.service_repository.update(dict(service))
                    break
            else:
                # never broke - no errors occurred - deploy
                self.service_repository.update(dict(service))
                self.deploy_service(service=service)

    def deploy_service(self, service):
        for image in service.images:
            image.id = self.zeromq_server.deploy_image(image)
        # store new image id
        self.service_repository.update(dict(service))

    def get_service_status(self, service):
        for image in service.images:
            image_status = self.zeromq_server.request_image_status(image)
            # TODO: calculate service state based on instance states

    def compare_capabilities(self, needed_capabilities, node_capabilities):
        """
        Compares two dicts with capabilities.

        :param needed_capabilities: the capabilities to compare with
        :param node_capabilities: the capabilties to check
        :return: True if all capabilities are fulfilled, otherwiese False
        """
        for capability in needed_capabilities:
            for node_capability in node_capabilities:
                if node_capability['label'] == capability:
                    # found them
                    break
            else:
                # never broke - capability not found - break outer loop and try next node
                return False
        return True

    def find_node(self, image):
        for node in self.node_repository.all():
            capabilities = self.zeromq_server.request_capabilities(node['ip'])
            if self.compare_capabilities(needed_capabilities=image.capabilities, node_capabilities=capabilities):
                return node
        return None

    def terminate_instances(self, service):
        """
        Terminates a service.

        :param service: the service to be used.
        """
        if service.action == Service.ServiceAction.REMOVE:
            if self.service_repository.has(service_id=service.id):
                service.state = Service.ServiceState.STOPPING
                self.service_repository.update(dict(service))
                for image in service.images:
                    self.zeromq_server.terminate_image(image)
            else:
                self.logger.error('Service `%s` with the id `%s` is not available' % (service.name, service.id))

    def handle_blueprint(self, blueprint_data):
        """
        Try to load the YAML data from the given blueprint data and validates them by using the
        ``motey.models.schemas.blueprint_yaml_schema``.
        If the data is valid, they will be transformed into a services model and handed over to the ``VALManager``.

        :param blueprint_data: data in YAML format which matches the ``motey.models.schemas.blueprint_yaml_schema``
        """
        try:
            loaded_data = yaml.load(blueprint_data)
            validate(loaded_data, blueprint_yaml_schema)
            service = Service.transform(loaded_data)
            worker_thread = None
            if service.action == Service.ServiceAction.ADD:
                worker_thread = threading.Thread(target=self.instantiate_service, args=(service,))
            elif service.action == Service.ServiceAction.REMOVE:
                worker_thread = threading.Thread(target=self.terminate_instances, args=(service,))
            else:
                self.logger.error(
                    'Action `%s` for service `%s` not a valid action type' % (service.action, service.name))

            if worker_thread:
                worker_thread.daemon = True
                worker_thread.start()

        except (yaml.YAMLError, ValidationError):
            self.logger.error('YAML file could not be parsed: %s' % blueprint_data)
