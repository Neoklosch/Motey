from yapsy.IPlugin import IPlugin

from motey.utils.logger import Logger


class AbstractVAL(IPlugin):
    def __init__(self):
        super().__init__()
        self.logger = Logger.Instance()

    def get_plugin_type(self):
        raise NotImplementedError("Should have implemented this")

    def has_image(self, image_name):
        raise NotImplementedError("Should have implemented this")

    def load_image(self, image_name):
        raise NotImplementedError("Should have implemented this")

    def delete_image(self, image_name):
        raise NotImplementedError("Should have implemented this")

    def create_instance(self, image_name, parameters={}):
        raise NotImplementedError("Should have implemented this")

    def start_instance(self, container_name, parameters={}):
        raise NotImplementedError("Should have implemented this")

    def stop_instance(self, container_name):
        raise NotImplementedError("Should have implemented this")

    def has_instance(self, container_name):
        raise NotImplementedError("Should have implemented this")

    def get_all_running_instances(self):
        raise NotImplementedError("Should have implemented this")

    def get_stats(self, container_name):
        raise NotImplementedError("Should have implemented this")

    def get_system_stats(self):
        raise NotImplementedError("Should have implemented this")

    def activate(self):
       self.logger.info("%s plugin activated" % self.get_plugin_type())

    def deactivate(self):
        self.logger.info("%s plugin deactivated" % self.get_plugin_type())
