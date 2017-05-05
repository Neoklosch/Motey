import os
from tinydb import TinyDB, Query
from decorators.singleton import Singleton

@Singleton
class LabelingEngine(object):
    def __init__(self):
        self.db = TinyDB(os.path.abspath("labels.json"))

    def getAllLabels(self):
        return self.db.all()

    def addLabel(self, label):
        if not self.hasLabel(label):
            self.db.insert({'label': label})

    def removeLabel(self, label):
        self.db.remove(Query().label == label)

    def clear(self):
        self.db.remove()

    def hasLabel(self, label):
        return len(self.db.search(Query().label == label)) > 0
