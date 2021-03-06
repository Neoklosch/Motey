import motey.val.plugins.abstractVAL as abstractVAL


class XenVAL(abstractVAL.AbstractVAL):
    def __init__(self):
        super().__init__()

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

    def has_instance(self, instance_name):
        raise NotImplementedError("Should have implemented this")

    def get_stats(self, container_name):
        raise NotImplementedError("Should have implemented this")
