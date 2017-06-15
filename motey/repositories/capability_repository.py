from tinydb import TinyDB, Query

from motey.configuration.configreader import config
from motey.repositories.base_repository import BaseRepository


class CapabilityRepository(BaseRepository):
    """
    Repository for all capability specific actions.
    """

    def __init__(self):
        """
        Start the ``TinyDB```instance and create or load the database.
        The database location can be configured via the ``config.ini`` file.
        """
        super(CapabilityRepository, self).__init__()
        self.db = TinyDB('%s/capabilities.json' % config['DATABASE']['path'])

    def add(self, capability, capability_type):
        """
        Add a new capability to the database.

        :param capability: the capability to be added.
        :param capability_type: the capability type of the capability.
        """
        if not self.has(capability):
            self.db.insert({'capability': capability, 'type': capability_type})

    def remove(self, capability, capability_type=None):
        """
        Remove a capability from the database.

        :param capability: the capability to be removed.
        :param capability_type: optional. The capability must also matche the capability type to be removed.
        """
        if capability_type:
            self.db.remove((Query().capability == capability) & (Query().type == capability_type))
        else:
            self.db.remove(Query().capability == capability)

    def remove_all_from_type(self, capability_type):
        """
        Remove a capabilities with a specific capability type.

        :param capability_type: the capability type where all related capabilitys should be removed.
        """
        self.db.remove(Query().type == capability_type)

    def has(self, capability):
        """
        Checks if the given ``capability`` exist in the database.

        :param capability: the capability to search for.
        :return: True if the lable exists, otherwise False
        """
        return len(self.db.search(Query().capability == capability)) > 0

    def has_type(self, capability_type):
        """
        Checks if a capability with the given ``capability_type`` exist in the database.

        :param capability_type: the type of the capability to search for.
        :return: True if the capability type exists, otherwise False
        """
        return len(self.db.search(Query().type == capability_type)) > 0
