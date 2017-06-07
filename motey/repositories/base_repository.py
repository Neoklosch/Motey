import os

from motey.configuration.configreader import config


class BaseRepository(object):
    """
    Base repository to wrapp database handling.
    """

    def __init__(self):
        """
        Constructor of the class.
        """
        self.db = None
        directory = os.path.abspath(config['DATABASE']['path'])
        if not os.path.exists(directory):
            os.makedirs(directory)

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
        self.db.purge()
