import uuid


class Service(object):
    class ServiceState(object):
        INITIAL = 0
        INSTANTIATING = 1
        RUNNING = 2
        STOPPING = 3
        TERMINATED = 4

    class ServiceAction(object):
        ADD = 'add'
        REMOVE = 'remove'

    class ServiceType(object):
        MASTER = 'master'
        SLAVE = 'slave'

    def __init__(self, name, images, id=uuid.uuid4().hex, state=ServiceState.INITIAL, action=ServiceAction.ADD, type=ServiceType.MASTER):
        self.id = id
        self.state = state
        self.action = action
        self.name = name
        self.images = images
        self.type = type
