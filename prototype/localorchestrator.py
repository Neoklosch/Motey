import yaml
from prototype.utils.logger import Logger
from prototype.decorators.singleton import Singleton
from prototype.val.valmanager import VALManager


@Singleton
class LocalOrchestrator(object):
    def __init__(self):
        self.logger = Logger.Instance()
        self.valmanager = VALManager.Instance()
        # self.blueprint_stream = BlueprintEndpoint.stream.subscribe(self.handle_blueprint)

    def get_heartbeat(self):
        pass

    def parse_template_file(self, template_path):
        with open(template_path, 'r') as stream:
            try:
                loaded_data = yaml.load(stream)
                if loaded_data and 'images' in loaded_data:
                    self.handle_images(loaded_data['images'])
            except yaml.YAMLError as exc:
                self.logger.error('YAML file could not be parsed: %s' % template_path)

    def exec_command_locally(self):
        pass

    def handle_images(self, images):
        for image in images:
            print(image)

    def handle_blueprint(self, schema):
        try:
            loaded_data = yaml.load(schema)
            if loaded_data and 'images' in loaded_data:
                self.handle_images(loaded_data['images'])
        except yaml.YAMLError as exc:
            self.logger.error('YAML file could not be parsed: %s' % schema)
