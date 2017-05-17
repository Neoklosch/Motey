from fog_node_engine.decorators.singleton import Singleton
from fog_node_engine.labeling.labelingengine import LabelingEngine


@Singleton
class HardwareEventEngine(object):
    def __init__(self):
        self.labeling_engine = LabelingEngine.Instance()

    def listen_for_events(self, event):
        self.labeling_engine.add_label(event, 'hardwareevent')
