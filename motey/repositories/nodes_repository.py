import os

from tinydb import TinyDB, Query

from motey.configuration.configreader import config
from motey.repositories.base_repository import BaseRepository


class NodesRepository(BaseRepository):
    """
    Repository for all node specific actions.
    """

    def __init__(self):
        """
        Start the ``TinyDB```instance and create or load the database.
        The database location can be configured via the ``config.ini`` file.
        """
        super(NodesRepository, self).__init__()
        self.db = TinyDB(os.path.abspath('%s/nodes.json' % config['DATABASE']['path']))

    def add(self, ip):
        """
        Add a new node to the database if they not exist yet.

        :param ip: the ip of the new node.
        """
        if not self.has(ip):
            self.db.insert({'ip': ip})

    def remove(self, ip):
        """
        Remove a node from the database.

        :param ip: the ip of the node to be removed.
        """
        self.db.remove(Query().ip == ip)

    def has(self, ip):
        """
        Checks if the given ``ip`` exist in the database.

        :param ip: the ip of the node to search for.
        :return: True if the node exists, otherwise False
        """
        return len(self.db.search(Query().ip == ip)) > 0
