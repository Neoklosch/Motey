from rx.subjects import Subject

from motey.utils.path_helper import absolute_file_path


class VALManager(object):
    """
    Manger for all the virtual abstraction layer plugins.
    Loads the plugins and wrapps the commands.
    """

    def __init__(self, logger, labeling_repository, plugin_manager):
        """
        Constructor of the VALManger.

        :param logger: DI injected
        :type logger: motey.utils.logger.Logger
        :param labeling_repository: the DI injected labeling engine instance
        :type labeling_repository: motey.repositories.labeling_repository.LabelingRepository
        :param plugin_manager: the DI injected plugin manager
        :type plugin_manager: yapsy.PluginManager.PluginManager
        """

        self.plugin_stream = Subject()
        self.logger = logger
        self.labeling_repository = labeling_repository
        self.plugin_manager = plugin_manager

    def start(self):
        """
        Starts the VALManager and register all the available plugins.
        """

        self.register_plugins()

    def register_plugins(self):
        """
        Register all the available plugins.
        A plugin has to be located under motey/val/plugins.
        After all the available plugins are loaded, the ``activate`` method of the plugin will be executed and a label
        with the related plugin type will be added to the labeling engine.
        """

        self.labeling_repository.remove_all_from_type('plugin')
        self.plugin_manager.setPluginPlaces([absolute_file_path("motey/val/plugins")])
        self.plugin_manager.collectPlugins()
        for plugin in self.plugin_manager.getAllPlugins():
            plugin.plugin_object.logger = self.logger
            plugin.plugin_object.activate()
            self.labeling_repository.add(plugin.plugin_object.get_plugin_type(), 'plugin')

    def instantiate(self, image, plugin_type):
        """
        Instantiate an image.

        :param image: the image which should be executed
        :type image: motey.models.image.Image
        :param plugin_type: Will only be executed with the given plugin
        :type plugin_type: str
        :return: the image id of the instantiated image
        """
        image_id = None
        for plugin in self.plugin_manager.getAllPlugins():
            if plugin_type and not plugin.plugin_object.get_plugin_type() == plugin_type:
                continue

            image_id = plugin.plugin_object.start_instance(image.name, image.parameters)
        return image_id

    def terminate(self, instance_name, plugin_type):
        """
        Terminate a running instance.

        :param instance_name: the name of the instance
        :type instance_name: str
        :param plugin_type: The instance will only be terminated for the given plugin
        :type plugin_type: str
        """
        for plugin in self.plugin_manager.getAllPlugins():
            if plugin_type and not plugin.plugin_object.get_plugin_type() == plugin_type:
                continue

            plugin.plugin_object.stop_instance(instance_name)

    def close(self):
        """
        Will clean up the VALManager.
        At first it will remove the label from the labeling engine and afterwards all the ``deactivate`` method for
        each plugin will be executed.
        """

        for plugin in self.plugin_manager.getAllPlugins():
            self.labeling_repository.remove(plugin.plugin_object.get_plugin_type())
            plugin.plugin_object.deactivate()
