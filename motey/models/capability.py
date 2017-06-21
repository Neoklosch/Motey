class Capability(object):
    """
    Model object. Represent a capability.
    """

    def __init__(self, capability, capability_type):
        """
        Constructor of the model object.

        :param capability: the name of the capability.
        :type capability: str
        :param capability_type: the type of the capability.
        :type capability_type: str
        """

        self.capability = capability
        self.capability_type = capability_type

    def __iter__(self):
        yield 'capability', self.capability
        yield 'capability_type', self.capability_type

    @staticmethod
    def transform(data):
        """
        Static method to translate a capability dict into a capability model.

        :param data: a dict with capability data
        :type data: dict
        :return: the translated capability model, None if something goes wrong
        """
        if 'capability' not in data or 'capability_type' not in data:
            return None
        return Capability(
            capability=data['capability'],
            capability_type=data['capability_type']
        )
