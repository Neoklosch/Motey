import os

from rx.subjects import Subject


class VALManager(object):
    """
    Manger for all the virtual abstraction layer plugins.
    Loads the plugins and wrapps the commands.
    """

    def __init__(self, logger, labeling_engine, plugin_manager):
        """
        Constructor of the VALManger.
        """

        self.plugin_stream = Subject()
        self.logger = logger
        self.labeling_engine = labeling_engine
        self.plugin_manager = plugin_manager
        self.register_plugins()

    def register_plugins(self):
        """
        Register all the available plugins.
        A plugin has to be located under motey/val/plugins.
        After all the available plugins are loaded, the ``activate`` method of the plugin will be executed and a label
        with the related plugin type will be added to the labeling engine.
        """

        self.labeling_engine.remove_all_from_type('plugin')
        self.plugin_manager.setPluginPlaces([os.path.abspath("motey/val/plugins")])
        self.plugin_manager.collectPlugins()
        for plugin in self.plugin_manager.getAllPlugins():
            plugin.plugin_object.activate()
            self.labeling_engine.add(plugin.plugin_object.get_plugin_type(), 'plugin')

    def instantiate(self, image_name, plugin_type=None):
        """
        Instantiate an image.

        :param image_name: The image_name can be type of str or list. The list can contain again str or a dict.
         If the image_name is a str, the instance with this specific name will be instantiated, if it a list with str in
         it, all the images in the list will be instanciated and if it is a list with a dict in it, each dict needs to
         have a key ``image_name```in it and an optional key ``parameters```which can be again a dict with different
         execution parameters.

         samples:
          image_name = 'alpine'
          image_name = ['alpine', 'busybox',]
          image_name = [{'image_name': 'alpine', 'parameters': {'ports': {'80/tcp': 8080}, 'name': 'motey_alpine'}},]
        :param plugin_type: Will only be executed with the given plugin. Must be a str. Default None.
        """

        for plugin in self.plugin_manager.getAllPlugins():
            if plugin_type and not plugin.plugin_object.get_plugin_type() == plugin_type:
                continue

            if isinstance(image_name, str):
                plugin.plugin_object.start_instance(image_name)
            elif isinstance(image_name, list):
                for single_image in image_name:
                    if isinstance(single_image, str):
                        plugin.plugin_object.start_instance(single_image)
                    elif isinstance(single_image, dict):
                        parameters = single_image['parameters'] if 'parameters' in single_image else {}
                        plugin.plugin_object.start_instance(single_image['image_name'], parameters)

    def terminate(self, instance_name, plugin_type=None):
        for plugin in self.plugin_manager.getAllPlugins():
            if plugin_type and not plugin.plugin_object.get_plugin_type() == plugin_type:
                continue

            if isinstance(instance_name, str):
                plugin.plugin_object.stop_instance(instance_name)
            elif isinstance(instance_name, list):
                for single_instance in instance_name:
                    plugin.plugin_object.stop_instance(single_instance)

    def close(self):
        """
        Will clean up the VALManager.
        At first it will remove the label from the labeling engine and afterwards all the ``deactivate`` method for
        each plugin will be executed.
        """

        for plugin in self.plugin_manager.getAllPlugins():
            self.labeling_engine.remove(plugin.plugin_object.get_plugin_type())
            plugin.plugin_object.deactivate()
