import yaml
from jsonschema import validate, ValidationError

from motey.communication.api_routes.blueprintendpoint import BlueprintEndpoint
from motey.decorators.singleton import Singleton
from motey.models.image import Image
from motey.models.service import Service
from motey.utils.logger import Logger
from motey.val.valmanager import VALManager
from motey.validation.schemas import blueprint_schema


@Singleton
class InterNodeOrchestrator(object):
    def __init__(self):
        self.logger = Logger.Instance()
        self.valmanager = VALManager.Instance()
        self.blueprint_stream = BlueprintEndpoint.stream.subscribe(self.handle_blueprint)

    def parse_template_file(self, template_path):
        with open(template_path, 'r') as stream:
            try:
                loaded_data = yaml.load(stream)
                validate(loaded_data, blueprint_schema)
                self.handle_images(loaded_data['images'])
            except (yaml.YAMLError, ValidationError):
                self.logger.error('YAML file could not be parsed: %s' % template_path)

    def exec_command_locally(self):
        pass

    def handle_images(self, images):
        self.valmanager.instantiate(images)

    def handle_blueprint(self, schema):
        try:
            loaded_data = yaml.load(schema)
            validate(loaded_data, blueprint_schema)
            service = self.__translate_to_service(loaded_data)
            self.handle_images(service.images)
        except (yaml.YAMLError, ValidationError):
            self.logger.error('YAML file could not be parsed: %s' % schema)

    def __translate_to_service(self, data):
        service = Service()
        service.name = data['service_name']
        service.images = self.__translate_to_image_list(data['images'])

    def __translate_to_image_list(self, data):
        result_list = []
        for image in data:
            result_list.append(self.__translate_to_image(image))
        return result_list

    def __translate_to_image(self, data):
        image = Image()
        image.name = data['image_name']
        image.parameters = data['parameters']
        image.capabilities = data['capabilities']
        return image
