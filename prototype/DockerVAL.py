import docker
from AbstractVAL import AbstractVAL

class DockerVAL(AbstractVAL):
    def __init__(self):
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    def hasImage(self, image_name):
        return image_name in self.client.images.list().id

    def getImage(self):
        raise NotImplementedError("Should have implemented this")

    def deleteImage(self):
        raise NotImplementedError("Should have implemented this")

    def startInstance(self):
        raise NotImplementedError("Should have implemented this")

    def stopInstance(self):
        raise NotImplementedError("Should have implemented this")

    def getStats(self):
        raise NotImplementedError("Should have implemented this")
