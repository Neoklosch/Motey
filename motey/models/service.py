import uuid


class Service(object):
    class ServiceState(object):
        INITIAL = 0
        INSTANTIATING = 1
        RUNNING = 2
        STOPPING = 3
        TERMINATED = 4

    def __init__(self, name, images, id=None, state=None):
        self.id = id if id else uuid.uuid4().hex
        self.state = state if state else self.ServiceState.INITIAL
        self.name = name
        self.images = images
