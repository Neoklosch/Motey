import os

from tinydb import TinyDB, Query

from motey.configuration.configreader import config
from motey.decorators.singleton import Singleton


class BaseRepository(object):
    """
    Base repository to wrapp database handling.
    This class is implemented as a Singleton and should be called via ``ServiceRepository.Instance()``.
    """

    def __init__(self):
        """
        Constructor of the class.
        """
        self.db = None

    def all(self):
        """
        Return a list of all existing entries in the database.

        :return: a list of all existing entries.
        """
        return self.db.all()

    def clear(self):
        """
        Remove all entries from the database.
        """
        self.db.remove()
