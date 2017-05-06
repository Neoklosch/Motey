from sanic import Sanic

app = Sanic()

class HardwareEventEngine(object):
    def __init__(self, labeling_engine):
        self.labeling_engine = labeling_engine
        app.run(host='0.0.0.0', port=5000)

    def listen_for_events(self, event):
        self.labeling_engine.addLabel(event, 'hardwareevent')
