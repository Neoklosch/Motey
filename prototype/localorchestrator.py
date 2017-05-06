import yaml

class LocalOrchestrator(object):
    def __init__(self, logger):
        self.logger = logger

    def parse_template(self, template_path):
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
