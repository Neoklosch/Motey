from yapsy.IPlugin import IPlugin


class AbstractVAL(IPlugin):
    def get_plugin__type(self):
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

    def getSystemStats(self):
        raise NotImplementedError("Should have implemented this")

    def activate(self):
        print("Plugin activated")

    def deactivate(self):
        print("Plugin deactivated")
