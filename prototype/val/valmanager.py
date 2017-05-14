import os
from rx.subjects import Subject
from yapsy.PluginManager import PluginManager
from prototype.decorators.singleton import Singleton
from prototype.labeling.labelingengine import LabelingEngine
from prototype.utils.logger import Logger


@Singleton
class VALManager(object):
    def __init__(self):
        self.plugin_stream = Subject()
        self.logger = Logger.Instance()
        self.labeling_engine = LabelingEngine.Instance()
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
            plugin.plugin_object.has_instance('keks')
            print(plugin.plugin_object.get_stats(plugin.plugin_object.get_all_running_instances()[0].id).ip)
        self.plugin_stream.on_next(42)

    def observe_commands(self):
        return self.plugin_stream

    def close(self):
        for plugin in self.plugin_manager.getAllPlugins():
            self.labeling_engine.remove_label(plugin.plugin_object.get_plugin__type())
            plugin.plugin_object.deactivate()
