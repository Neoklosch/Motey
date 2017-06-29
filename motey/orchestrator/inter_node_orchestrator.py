import threading

from motey.communication.api_routes.service import Service as ServiceEndpoint
from motey.models.image_state import ImageState
from motey.models.service_state import ServiceState
from motey.utils.network_utils import get_own_ip


class InterNodeOrchestrator(object):
    """
    This class orchestrates services.
    It will start and stop virtual instances of images defined in the service.
    It also can communicate with other nodes to start instances there if the requirements does not fit with the
    possibilities of the current node.
    """

    def __init__(self, logger, valmanager, service_repository, capability_repository, node_repository,
                 communication_manager):
        """
        Constructor of the class.

        :param logger: DI injected
        :type logger: motey.utils.logger.Logger
        :param valmanager: DI injected
        :type valmanager: motey.val.valmanager.VALManager
        :param service_repository: DI injected
        :type service_repository: motey.repositories.service_repository.ServiceRepository
        :param capability_repository: DI injected
        :type capability_repository: motey.capabilityengine.capabiltiy_engine.CapabilityEngine
        :param node_repository: DI injected
        :type node_repository: motey.repositories.node_repository.NodeRepository
        :param communication_manager: DI injected
        :type communication_manager: motey.communication.communication_manager.CommunicationManager
        """
        self.logger = logger
        self.valmanager = valmanager
        self.service_repository = service_repository
        self.capability_repository = capability_repository
        self.node_repository = node_repository
        self.communication_manager = communication_manager
        self.blueprint_stream = ServiceEndpoint.yaml_post_stream.subscribe(self.instantiate_service)
        self.blueprint_stream = ServiceEndpoint.yaml_delete_stream.subscribe(self.terminate_service)

    def instantiate_service(self, service):
        """
        Instantiate a service.

        :param service: the service to be used.
        :type service: motey.models.service.Service
        """

        def __inner_instantiate(inner_service):
            """
            Inner function which is used to run in a thread to instantiate a service.

            :param inner_service: the service to be used.
            :type inner_service: motey.models.service.Service
            """
            inner_service.state = ServiceState.INSTANTIATING
            self.service_repository.add(dict(inner_service))
            for image in inner_service.images:
                if not image.capabilities:
                    # no capabilities, deploy locally
                    image.node = get_own_ip()
                    continue

                for capability in image.capabilities:
                    if not self.capability_repository.has(capability=capability):
                        # if a single capability is not satisfied, search for external node
                        node = self.find_node(image)
                        if node:
                            image.node = node['ip']
                            # found a node which handle the container - we can break the loop
                            break
                        else:
                            # does not found any node - error
                            inner_service.state = ServiceState.ERROR
                            break
                else:
                    # never broke - all capabilities are succeeded locally
                    image.node = get_own_ip()

                if inner_service.state == ServiceState.ERROR:
                    self.service_repository.update(dict(inner_service))
                    break
            else:
                # never broke - no errors occurred - deploy
                self.service_repository.update(dict(inner_service))
                self.deploy_service(service=inner_service)

        worker_thread = threading.Thread(target=__inner_instantiate, args=(service,))
        worker_thread.daemon = True
        worker_thread.start()

    def deploy_service(self, service):
        """
        Deploy all images of a service to the related nodes.

        :param service: the service which should be deployed
        :type service: motey.models.service.Service
        """
        for image in service.images:
            image.id = self.communication_manager.deploy_image(image)
        # store new image id
        self.service_repository.update(dict(service))

    def get_service_status(self, service):
        """
        Returns the service status.

        :param service: the service which should be used
        :type service: motey.models.service.Service
        :return: the status of the service
        """
        image_status_list = []
        for image in service.images:
            image_status = self.communication_manager.request_image_status(image)
            image_status_list.append(image_status)

        if ImageState.ERROR in image_status_list:
            service.state = ServiceState.ERROR
            self.terminate_service(service=service)
        elif ImageState.TERMINATED in image_status_list:
            service.state = ServiceState.TERMINATED
            self.terminate_service(service=service)
        elif ImageState.STOPPING in image_status_list:
            service.state = ServiceState.STOPPING
            self.terminate_service(service=service)
        elif ImageState.INSTANTIATING in image_status_list:
            service.state = ServiceState.INSTANTIATING
        elif ImageState.INITIAL in image_status_list:
            service.state = ServiceState.INITIAL
        elif len(image_status_list) > 0 and image_status_list[1:] == image_status_list[:-1] and \
                image_status_list[0] == ImageState.RUNNING:
            service.state = ServiceState.RUNNING
        else:
            service.state = ServiceState.ERROR

        self.service_repository.update(dict(service))
        return service.state

    def compare_capabilities(self, needed_capabilities, node_capabilities):
        """
        Compares two dicts with capabilities.

        :param needed_capabilities: the capabilities to compare with
        :type needed_capabilities: dict
        :param node_capabilities: the capabilties to check
        :type node_capabilities: dict
        :return: True if all capabilities are fulfilled, otherwiese False
        """
        for capability in needed_capabilities:
            for node_capability in node_capabilities:
                if node_capability['capability'] == capability:
                    # found them
                    break
            else:
                # never broke - capability not found - break outer loop and try next node
                return False
        return True

    def find_node(self, image):
        """
        Try to find a node in the cluster which can be used to deploy the given image.

        :param image: the image to be used
        :type image: motey.models.image.Image
        :return: the IP of the node to be used or None if it does not found a node which fulfill all capabilities
        """
        for node in self.node_repository.all():
            capabilities = self.communication_manager.request_capabilities(node['ip'])
            if self.compare_capabilities(needed_capabilities=image.capabilities, node_capabilities=capabilities):
                return node
        return None

    def terminate_service(self, service):
        """
        Terminates a service.

        :param service: the service to be used.
        :type service: motey.models.service.Service
        """

        def __inner_terminate(inner_service):
            """
            Inner function which is used to run in a thread to terminates a service.

            :param inner_service: the service to be used.
            :type inner_service: motey.models.service.Service
            """
            if self.service_repository.has(service_id=inner_service.id):
                inner_service.state = ServiceState.STOPPING
                self.service_repository.update(dict(inner_service))
                for image in inner_service.images:
                    self.communication_manager.terminate_image(image)
            else:
                self.logger.error(
                    'Service `%s` with the id `%s` is not available' % (inner_service.service_name, inner_service.id))

        worker_thread = threading.Thread(target=__inner_terminate, args=(service,))
        worker_thread.daemon = True
        worker_thread.start()
