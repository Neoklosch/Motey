import uuid

from motey.models.image import Image


class Service(object):
    """
    Model object. Represent a service.
    A service can have multiple states, action types and service types.
    """

    class ServiceState(object):
        """
        Enum with service states.
         * INITIAL
         * INSTANTIATING
         * RUNNING
         * STOPPING
         * TERMINATED
         * ERROR
        """
        INITIAL = 0
        INSTANTIATING = 1
        RUNNING = 2
        STOPPING = 3
        TERMINATED = 4
        ERROR = 5

    class ServiceAction(object):
        """
        Enum with action types.
         * ADD
         * REMOVE
        """
        ADD = 'add'
        REMOVE = 'remove'

    class ServiceType(object):
        """
        Enum with service types.
         * MASTER
         * SLAVE
        """
        MASTER = 'master'
        SLAVE = 'slave'

    def __init__(self, name, images, id=uuid.uuid4().hex, state=ServiceState.INITIAL, action=ServiceAction.ADD,
                 node_type=ServiceType.MASTER):
        """
        Constructor of the service model.

        :param name: the name of the service
        :type name: str
        :param images: list of images which are asociated with the service
        :type images: list
        :param id: autogenerated id of the service
        :type id: uuid
        :param state: current state of the service. Default `INITIAL`.
        :type state: motey.models.service.Service.ServiceState
        :param action: action type of the service. Default `ADD`.
        :type action: motey.models.service.Service.ServiceAction
        :param node_type: node type of the service. Default `MASER`.
        :type node_type: motey.models.service.Service.ServiceType
        """

        self.id = id
        self.state = state
        self.action = action
        self.name = name
        self.images = images
        self.node_type = node_type

    def __iter__(self):
        yield 'id', self.id
        yield 'state', self.state
        yield 'action', self.action
        yield 'node_type', self.node_type
        yield 'images', [dict(image) for image in self.images]

    @staticmethod
    def transform(data):
        """
        Static method to translate the service dict data into a service model.

        :param data: service dict to be transformed
        :type data: dict
        :return: the translated service model, None if something went wrong
        """
        if 'service_name' not in data or 'images' not in data:
            return None
        return Service(
            name=data['service_name'],
            images=[Image.transform(image) for image in data['images']],
            id=data['id'] if 'id' in data else uuid.uuid4().hex,
            state=data['state'] if 'state' in data else Service.ServiceState.INITIAL,
            action=data['action'] if 'action' in data else Service.ServiceAction.ADD,
            node_type=data['node_type'] if 'node_type' in data else Service.ServiceType.MASTER
        )
