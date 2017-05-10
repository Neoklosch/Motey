import os
from rx.subjects import Subject
from yapsy.PluginManager import PluginManager


class VALManager(object):
    def __init__(self, logger, labeling_engine, local_orchestrator):
        self.plugin_stream = Subject()
        self.logger = logger
        self.labeling_engine = labeling_engine
        self.local_orchestrator = local_orchestrator
        self.plugin_manager = PluginManager()
        self.register_plugins()

    def register_plugins(self):
        self.labeling_engine.removeAllFromType('plugin')
        self.plugin_manager.setPluginPlaces([os.path.abspath("valplugins")])
        self.plugin_manager.collectPlugins()
        for plugin in self.plugin_manager.getAllPlugins():
            plugin.plugin_object.activate()
            self.labeling_engine.addLabel(plugin.plugin_object.getPluginType(), 'plugin')

    def get_active_vals(self):
        pass

    def exec_command(self):
        self.plugin_stream.on_next(42)

    def observe_commands(self):
        return self.plugin_stream

    def close(self):
        for plugin in self.plugin_manager.getAllPlugins():
            self.labeling_engine.removeLabel(plugin.plugin_object.getPluginType())
            plugin.plugin_object.deactivate()
