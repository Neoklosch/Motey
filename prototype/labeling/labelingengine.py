import os
from tinydb import TinyDB, Query
from decorators.singleton import Singleton

@Singleton
class LabelingEngine(object):
    def __init__(self):
        self.db = TinyDB(os.path.abspath("data/labels.json"))

    def getAllLabels(self):
        return self.db.all()

    def addLabel(self, label, label_type):
        if not self.hasLabel(label):
            self.db.insert({'label': label, 'type': label_type})

    def removeLabel(self, label, label_type = None):
        if label_type:
            self.db.remove((Query().label == label) & (Query().type == label_type))
        else:
            self.db.remove(Query().label == label)

    def removeAllFromType(self, label_type):
        self.db.remove(Query().type == label_type)

    def clear(self):
        self.db.remove()

    def hasLabel(self, label):
        return len(self.db.search(Query().label == label)) > 0

    def hasType(self, label_type):
        return len(self.db.search(Query().type == label_type)) > 0
