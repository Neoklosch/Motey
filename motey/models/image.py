class Image(object):
    """
    Model object. Represent an image.
    An image can have execution parameters, required capabilities and the node where it is executed.
    All of them are optional.
    """

    def __init__(self, name, id='', parameters={}, capabilities={}, node=None):
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
        """

        self.id = id
        self.name = name
        self.parameters = parameters
        self.capabilities = capabilities
        self.node = node
