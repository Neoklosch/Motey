from motey.database.labeling_database import LabelingDatabase
from motey.decorators.singleton import Singleton


@Singleton
class HardwareEventEngine(object):
    def __init__(self):
        self.labeling_engine = LabelingDatabase.Instance()

    def listen_for_events(self, event):
        self.labeling_engine.add(event, 'hardwareevent')
