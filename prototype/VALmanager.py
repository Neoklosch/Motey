import os
from rx.subjects import Subject
from yapsy.PluginManager import PluginManager

class VALManager(object):
    def __init__(self, labeling_engine):
        self.plugin_stream = Subject()
        self.labeling_engine = labeling_engine
        self.plugin_manager = PluginManager()
        self.plugin_manager.setPluginPlaces([os.path.abspath("valplugins")])
        self.plugin_manager.collectPlugins()
        for plugin in self.plugin_manager.getAllPlugins():
            print(plugin.plugin_object)
            self.labeling_engine.addLabel(plugin.plugin_object.getPluginType())

    def getActiveVALs(self):
        pass

    def execCommand(self):
        self.plugin_stream.on_next(42)

    def observeCommands(self):
        return self.plugin_stream
