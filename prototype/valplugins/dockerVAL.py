import docker
import valplugins.abstractVAL as abstractVAL

class DockerVAL(abstractVAL.AbstractVAL):
    def __init__(self):
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    def getPluginType(self):
        return 'docker'

    def hasImage(self, image_name):
        for image in self.client.images.list():
            if image.id == image_name or image.short_id == image_name or \
            image.id == 'sha256:%s' % image_name or image.short_id == 'sha256:%s' % image_name:
                return True
        return False

    def loadImage(self, image_name):
        self.client.images.pull(image_name)

    def deleteImage(self, image_name):
        self.client.images.remove(image_name)

    def createInstance(self, image_name):
        self.client.containers.create(image_name)

    def startInstance(self, container_name):
        self.client.containers.run(container_name)

    def stopInstance(self, container_name):
        self.client.containers.run(container_name)

    def getStats(self, container_name):
        raise NotImplementedError("Should have implemented this")
