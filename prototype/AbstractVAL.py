class AbstractVAL(object):
    def hasImage(self):
        raise NotImplementedError("Should have implemented this")

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
