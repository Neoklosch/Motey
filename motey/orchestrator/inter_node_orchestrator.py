import threading

import yaml
from jsonschema import validate, ValidationError

from motey.communication.api_routes.blueprintendpoint import BlueprintEndpoint
from motey.decorators.singleton import Singleton
from motey.models.image import Image
from motey.models.service import Service
from motey.repositories.service_repository import ServiceRepository
from motey.utils.logger import Logger
from motey.val.valmanager import VALManager
from motey.validation.schemas import blueprint_schema


@Singleton
class InterNodeOrchestrator(object):
    """
    This class orchestrates yaml blueprints.
    It will start and stop virtual instances of images defined in the blueprint.
    It also can communicate with other nodes to start instances there if the requirements does not fit with the
    possibilities of the current node.
    This class is implemented as a Singleton and should be called via InterNodeOrchestrator.Instance().
    """
    def __init__(self):
        """
        Instantiates the ``Logger``, the ``VALManagger``, ``ServiceRepository`` and subscribe to the blueprint endpoint.
        """
        self.logger = Logger.Instance()
        self.valmanager = VALManager.Instance()
        self.service_repository = ServiceRepository.Instance()
        self.blueprint_stream = BlueprintEndpoint.yaml_post_stream.subscribe(self.handle_blueprint)

    def parse_local_blueprint_file(self, file_path):
        """
        Parse a local yaml file and start the virtual images defined in the blueprint.

        :param file_path: Path to the local blueprint file.
        """
        with open(file_path, 'r') as stream:
            self.handle_blueprint(stream)

    def handle_images(self, service):
        """
        Instantiate a list of images.

        :param images: a list of images.
        """
        self.service_repository.add(service)
        service.state = Service.ServiceState.INSTANTIATING
        self.service_repository.update(service)
        for image in service.images:
            self.valmanager.instantiate(image)
        service.state = Service.ServiceState.RUNNING
        self.service_repository.update(service)

    def handle_blueprint(self, blueprint_data):
        """
        Try to load the YAML data from the given blueprint data and validates them by using the
        ``validation.schemas.blueprint_schema``.
        If the data is valid, they will be transformed into a services model and handed over to the ``VALManager``.

        :param blueprint_data: data in YAML format which matches the ``validation.schemas.blueprint_schema``
        """
        try:
            loaded_data = yaml.load(blueprint_data)
            validate(loaded_data, blueprint_schema)
            service = self.__translate_to_service(loaded_data)
            worker_thread = threading.Thread(target=self.handle_images, args=(service,))
            worker_thread.daemon = True
            worker_thread.start()
        except (yaml.YAMLError, ValidationError):
            self.logger.error('YAML file could not be parsed: %s' % blueprint_data)

    def __translate_to_service(self, blueprint_data):
        """
        Private method to translate the blueprint data into a service model.

        :param blueprint_data: data in YAML format which matches the ``validation.schemas.blueprint_schema``
        :return: the translated service model
        """
        service = Service()
        service.name = blueprint_data['service_name']
        service.images = self.__translate_to_image_list(blueprint_data['images'])
        return service

    def __translate_to_image_list(self, yaml_data):
        """
        Priavte method to translate a list of images into a list of image models.

        :param yaml_data: list of images which should be translated
        :return: a list of translated image models
        """
        result_list = []
        for image in yaml_data:
            result_list.append(self.__translate_to_image(image))
        return result_list

    def __translate_to_image(self, yaml_data):
        """
        Private method to translate a single yaml image data into a image model.

        :param yaml_data: a single yaml image data
        :return: the translated image model
        """
        image = Image()
        image.name = yaml_data['image_name']
        image.parameters = yaml_data['parameters']
        image.capabilities = yaml_data['capabilities']
        return image
