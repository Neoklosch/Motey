class Image(object):
    def __init__(self, name, id='', parameters={}, capabilities={}, node=None):
        self.id = id
        self.name = name
        self.parameters = parameters
        self.capabilities = capabilities
        self.node = node
