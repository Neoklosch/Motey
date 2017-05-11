class HardwareEventEngine(object):
    def __init__(self, labeling_engine):
        self.labeling_engine = labeling_engine

    def listen_for_events(self, event):
        self.labeling_engine.add_label(event, 'hardwareevent')
