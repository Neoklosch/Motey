from rx.subjects import Subject

class VALManager(object):
    def __init__(self):
        self.plugin_stream = Subject()

    def getActiveVALs(self):
        pass

    def execCommand(self):
        self.plugin_stream.on_next(42)

    def observeCommands(self):
        return self.plugin_stream
