class Image(object):
    """
    Model object. Represent an image.
    An image can have execution parameters, required capabilities and the node where it is executed.
    All of them are optional.
    """

    class ImageState(object):
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

    def __init__(self, name, id='', parameters={}, capabilities={}, node=None, state=ImageState.INITIAL):
        """
        Construcotr of the model object.

        :param name: the name of the image. Mostly related to the VAL plugin.
        :type name: str
        :param id: the id of the executed image instance. Mostly related to the VAL plugin.
        :type id: str
        :param parameters: a dict with one or multiple execution parameters. Default empty dict.
        :type parameters: dict
        :param capabilities: a dict with one or multiple capabilities which are necessary for running the image. Default
                             empty dict.
        :type capabilities: dict
        :param node: the node where the image is executed. Default None which is equivalent to the current node.
        :type node: str
        :param state: current state of the image. Default `INITIAL`.
        :type state: motey.models.image.Image.ImageState
        """

        self.id = id
        self.name = name
        self.parameters = parameters
        self.capabilities = capabilities
        self.node = node
        self.status = state

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'parameters', self.parameters
        yield 'capabilities', self.capabilities
        yield 'status', self.status

    @staticmethod
    def transform(json_data):
        if 'name' not in json_data:
            return None
        return Image(
            name=json_data['name'],
            id=json_data['id'] if 'id' in json_data else '',
            parameters=json_data['parameters'] if 'parameters' in json_data else {},
            capabilities=json_data['capabilities'] if 'capabilities' in json_data else {},
            node=json_data['node'] if 'node' in json_data else {},
            state=json_data['state'] if 'state' in json_data else {}
        )
