import os
from rx.subjects import Subject
from yapsy.PluginManager import PluginManager


class VALManager(object):
    def __init__(self, logger, labeling_engine):
        self.plugin_stream = Subject()
        self.logger = logger
        self.labeling_engine = labeling_engine
        self.plugin_manager = PluginManager()
        self.register_plugins()

    def register_plugins(self):
        self.labeling_engine.remove_all_from_type('plugin')
        self.plugin_manager.setPluginPlaces([os.path.abspath("prototype/val/plugins")])
        self.plugin_manager.collectPlugins()
        for plugin in self.plugin_manager.getAllPlugins():
            plugin.plugin_object.activate()
            self.labeling_engine.add_label(plugin.plugin_object.get_plugin__type(), 'plugin')

    def get_active_vals(self):
        pass

    def exec_command(self):
        for plugin in self.plugin_manager.getAllPlugins():
            print(plugin.plugin_object.get_stats('4157ad15a9e9').ip)
        self.plugin_stream.on_next(42)

    def observe_commands(self):
        return self.plugin_stream

    def close(self):
        for plugin in self.plugin_manager.getAllPlugins():
            self.labeling_engine.remove_label(plugin.plugin_object.get_plugin__type())
            plugin.plugin_object.deactivate()
