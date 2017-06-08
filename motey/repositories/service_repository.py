import os

from tinydb import TinyDB, Query

from motey.configuration.configreader import config
from motey.repositories.base_repository import BaseRepository


class ServiceRepository(BaseRepository):
    """
    Repository for all service specific actions.
    """

    def __init__(self):
        """
        Start the ``TinyDB```instance and create or load the database.
        The database location can be configured via the ``config.ini`` file.
        """
        super(ServiceRepository, self).__init__()
        self.db = TinyDB(os.path.abspath('%s/services.json' % config['DATABASE']['path']))

    def add(self, service):
        """
        Add a new service to the database if they not exist yet.

        :param service: a service model to be stored
        """
        if not self.has(service['id']):
            self.db.insert(service)

    def update(self, service):
        self.db.update(service, Query().id == service['id'])

    def remove(self, service_id):
        """
        Remove a service from the database.

        :param service_id: the id of the service to be removed.
        """
        self.db.remove(Query().id == service_id)

    def has(self, service_id):
        """
        Checks if the given ``id`` exist in the database.

        :param service_id: the id of the service to search for.
        :return: True if the service exists, otherwise False
        """
        return len(self.db.search(Query().id == service_id)) > 0
