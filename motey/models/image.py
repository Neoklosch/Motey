class Image(object):
    """
    Model object. Represent an image.
    An image can have execution parameters, required capabilities and the node where it is executed.
    All of them are optional.
    """

    def __init__(self, name, engine, id='', parameters={}, capabilities={}, node=None):
        """
        Constructor of the model object.

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
        :type node: dict
        """

        self.id = id
        self.name = name
        self.engine = engine
        self.parameters = parameters
        self.capabilities = capabilities
        self.node = node

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'engine', self.engine
        yield 'parameters', self.parameters
        yield 'capabilities', self.capabilities
        yield 'node', self.node

    @staticmethod
    def transform(data):
        """
        Static method to translate an image dict into a image model.

        :param data: a dict with image data
        :type data: dict
        :return: the translated image model, None if something goes wrong
        """
        if 'name' not in data or 'engine' not in data:
            return None
        return Image(
            name=data['name'],
            engine=data['engine'],
            id=data['id'] if 'id' in data else '',
            parameters=data['parameters'] if 'parameters' in data else {},
            capabilities=data['capabilities'] if 'capabilities' in data else {},
            node=data['node'] if 'node' in data else {}
        )
