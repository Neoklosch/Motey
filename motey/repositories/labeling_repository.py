import os

from tinydb import TinyDB, Query

from motey.configuration.configreader import config
from motey.decorators.singleton import Singleton


@Singleton
class LabelingRepository(object):
    """
    Repository for all label specific actions.
    This class is implemented as a Singleton and should be called via LabelingRepository.Instance().
    """

    def __init__(self):
        """
        Start the ``TinyDB```instance and create or load the database.
        The database location can be configured via the ``config.ini`` file.
        """
        self.db = TinyDB(os.path.abspath('%s/labels.json' % config['DATABASE']['path']))

    def all(self):
        """
        Return a list of all existing label entries in the database.

        :return: a list of all existing label entries.
        """
        return self.db.all()

    def add(self, label, label_type):
        """
        Add a new label to the database.

        :param label: the label to be added.
        :param label_type: the label type of the label.
        """
        if not self.has(label):
            self.db.insert({'label': label, 'type': label_type})

    def remove(self, label, label_type=None):
        """
        Remove a label from the database.

        :param label: the label to be removed.
        :param label_type: optional. The label must also matche the label type to be removed.
        """
        if label_type:
            self.db.remove((Query().label == label) & (Query().type == label_type))
        else:
            self.db.remove(Query().label == label)

    def remove_all_from_type(self, label_type):
        """
        Remove a labels with a specific label type.

        :param label_type: the label type where all related labels should be removed.
        """
        self.db.remove(Query().type == label_type)

    def clear(self):
        """
        Remove all label from the database.
        """
        self.db.remove()

    def has(self, label):
        """
        Checks if the given ``label`` exist in the database.

        :param ip: the label to search for.
        :return: True if the lable exists, otherwise False
        """
        return len(self.db.search(Query().label == label)) > 0

    def has_type(self, label_type):
        """
        Checks if a label with the given ``label_type`` exist in the database.

        :param label_type: the type of the label to search for.
        :return: True if the label type exists, otherwise False
        """
        return len(self.db.search(Query().type == label_type)) > 0
