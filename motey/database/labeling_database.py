import os

from tinydb import TinyDB, Query

from motey.configuration.configreader import config
from motey.decorators.singleton import Singleton


@Singleton
class LabelingDatabase(object):
    def __init__(self):
        self.db = TinyDB(os.path.abspath('%s/labels.json' % config['DATABASE']['path']))

    def all(self):
        return self.db.all()

    def add(self, label, label_type):
        if not self.has(label):
            self.db.insert({'label': label, 'type': label_type})

    def remove(self, label, label_type=None):
        if label_type:
            self.db.remove((Query().label == label) & (Query().type == label_type))
        else:
            self.db.remove(Query().label == label)

    def remove_all_from_type(self, label_type):
        self.db.remove(Query().type == label_type)

    def clear(self):
        self.db.remove()

    def has(self, label):
        return len(self.db.search(Query().label == label)) > 0

    def has_type(self, label_type):
        return len(self.db.search(Query().type == label_type)) > 0
