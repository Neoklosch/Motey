import os

from rx.subjects import Subject
from yapsy.PluginManager import PluginManager

from motey.database.labeling_database import LabelingDatabase
from motey.decorators.singleton import Singleton
from motey.utils.logger import Logger


@Singleton
class VALManager(object):
    def __init__(self):
        self.plugin_stream = Subject()
        self.logger = Logger.Instance()
        self.labeling_engine = LabelingDatabase.Instance()
        self.plugin_manager = PluginManager()
        self.register_plugins()

    def register_plugins(self):
        self.labeling_engine.remove_all_from_type('plugin')
        self.plugin_manager.setPluginPlaces([os.path.abspath("motey/val/plugins")])
        self.plugin_manager.collectPlugins()
        for plugin in self.plugin_manager.getAllPlugins():
            plugin.plugin_object.activate()
            self.labeling_engine.add(plugin.plugin_object.get_plugin__type(), 'plugin')

    def get_active_vals(self):
        pass

    def instantiate(self, image_name):
        for plugin in self.plugin_manager.getAllPlugins():
            print(image_name)
            if isinstance(image_name, str):
                plugin.plugin_object.start_instance(image_name)
            elif isinstance(image_name, list):
                for single_image in image_name:
                    if isinstance(single_image, str):
                        plugin.plugin_object.start_instance(single_image)
                    elif isinstance(single_image, dict):
                        print("image name: %s" % single_image['image_name'])
                        print("parameters: %s" % single_image['parameters'])
                        parameters = single_image['parameters'] if 'parameters' in single_image else {}
                        plugin.plugin_object.start_instance(single_image['image_name'], parameters)

    def exec_command(self):
        for plugin in self.plugin_manager.getAllPlugins():
            pass
            # TODO: exec real commands
            # getattr(plugin.plugin_object, 'bar')()
            # print(plugin.plugin_object.get_stats(plugin.plugin_object.get_all_running_instances()[0].id).ip)
            # system_stats = plugin.plugin_object.get_system_stats()
            # print(system_stats.used_memory)
            # print(system_stats.used_cpu)
            # print(system_stats.network_tx_bytes)
            # print(system_stats.network_rx_bytes)
        self.plugin_stream.on_next(42)

    def observe_commands(self):
        return self.plugin_stream

    def close(self):
        for plugin in self.plugin_manager.getAllPlugins():
            self.labeling_engine.remove(plugin.plugin_object.get_plugin__type())
            plugin.plugin_object.deactivate()
