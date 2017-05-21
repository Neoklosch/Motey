import yaml

from motey.communication.api_routes.blueprintendpoint import BlueprintEndpoint
from motey.decorators.singleton import Singleton
from motey.utils.logger import Logger
from motey.val.valmanager import VALManager
from jsonschema import validate, ValidationError
from motey.validation.schemas import blueprint_schema


@Singleton
class InterNodeOrchestrator(object):
    def __init__(self):
        self.logger = Logger.Instance()
        self.valmanager = VALManager.Instance()
        self.blueprint_stream = BlueprintEndpoint.stream.subscribe(self.handle_blueprint)

    def get_heartbeat(self):
        pass

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
            self.handle_images(loaded_data['images'])
        except (yaml.YAMLError, ValidationError):
            self.logger.error('YAML file could not be parsed: %s' % schema)
