from fog_node_engine.database.labeling_database import LabelingDatabase
from fog_node_engine.decorators.singleton import Singleton


@Singleton
class HardwareEventEngine(object):
    def __init__(self):
        self.labeling_engine = LabelingDatabase.Instance()

    def listen_for_events(self, event):
        self.labeling_engine.add(event, 'hardwareevent')
