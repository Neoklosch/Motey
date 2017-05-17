import os
from tinydb import TinyDB, Query
from fog_node_engine.decorators.singleton import Singleton


@Singleton
class LabelingEngine(object):
    def __init__(self):
        self.db = TinyDB(os.path.abspath("fog_node_engine/data/labels.json"))

    def get_all_labels(self):
        return self.db.all()

    def add_label(self, label, label_type):
        if not self.has_label(label):
            self.db.insert({'label': label, 'type': label_type})

    def remove_label(self, label, label_type=None):
        if label_type:
            self.db.remove((Query().label == label) & (Query().type == label_type))
        else:
            self.db.remove(Query().label == label)

    def remove_all_from_type(self, label_type):
        self.db.remove(Query().type == label_type)

    def clear(self):
        self.db.remove()

    def has_label(self, label):
        return len(self.db.search(Query().label == label)) > 0

    def has_type(self, label_type):
        return len(self.db.search(Query().type == label_type)) > 0
