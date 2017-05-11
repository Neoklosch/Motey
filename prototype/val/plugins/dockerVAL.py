import docker

import prototype.val.plugins.abstractVAL as abstractVAL


class DockerVAL(abstractVAL.AbstractVAL):
    def __init__(self):
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    def get_plugin__type(self):
        return 'docker'

    def has_image(self, image_name):
        for image in self.client.images.list():
            if image.id == image_name or image.short_id == image_name or image.id == 'sha256:%s' % image_name or image.short_id == 'sha256:%s' % image_name:
                return True
        return False

    def load_image(self, image_name):
        self.client.images.pull(image_name)

    def delete_image(self, image_name):
        self.client.images.remove(image_name)

    def create_instance(self, image_name):
        self.client.containers.create(image_name)

    def start_instance(self, container_name):
        self.client.containers.run(container_name)

    def stop_instance(self, container_name):
        self.client.containers.run(container_name)

    def has_instance(self, container_name):
        raise NotImplementedError("Should have implemented this")

    def get_stats(self, container_name):
        raise NotImplementedError("Should have implemented this")
