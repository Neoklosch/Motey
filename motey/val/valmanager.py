from rx.subjects import Subject

from motey.models.image import Image
from motey.utils.path_helper import absolute_file_path


class VALManager(object):
    """
    Manger for all the virtual abstraction layer plugins.
    Loads the plugins and wrapps the commands.
    """

    def __init__(self, logger, capability_repository, plugin_manager):
        """
        Constructor of the VALManger.

        :param logger: DI injected
        :type logger: motey.utils.logger.Logger
        :param capability_repository: the DI injected capability engine instance
        :type capability_repository: motey.repositories.capability_repository.CapabilityRepository
        :param plugin_manager: the DI injected plugin manager
        :type plugin_manager: yapsy.PluginManager.PluginManager
        """

        self.plugin_stream = Subject()
        self.logger = logger
        self.capability_repository = capability_repository
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
        After all the available plugins are loaded, the ``activate`` method of the plugin will be executed and a
        capability with the related plugin type will be added to the capability engine.
        """

        self.capability_repository.remove_all_from_type('plugin')
        self.plugin_manager.setPluginPlaces(directories_list=[absolute_file_path("motey/val/plugins")])
        self.plugin_manager.collectPlugins()
        for plugin in self.plugin_manager.getAllPlugins():
            plugin.plugin_object.logger = self.logger
            plugin.plugin_object.activate()
            self.capability_repository.add(capability=plugin.plugin_object.get_plugin_type(), capability_type='plugin')

    def instantiate(self, image):
        """
        Instantiate an image.

        :param image: the image which should be executed
        :type image: motey.models.image.Image
        :return: the image id of the instantiated image
        """
        image_id = None
        for plugin in self.plugin_manager.getAllPlugins():
            if image.engine and not plugin.plugin_object.get_plugin_type() == image.engine:
                continue

            image_id = plugin.plugin_object.start_instance(instance_name=image.name, parameters=image.parameters)
        return image_id

    def get_instance_state(self, image):
        state = Image.ImageState.ERROR
        for plugin in self.plugin_manager.getAllPlugins():
            if image.engine and not plugin.plugin_object.get_plugin_type() == image.engine:
                continue
            state = plugin.plugin_object.get_image_instance_state()
        return state

    def terminate(self, image):
        """
        Terminate a running instance.

        :param instance_name: the name of the instance
        :type instance_name: str
        """
        for plugin in self.plugin_manager.getAllPlugins():
            if image.engine and not plugin.plugin_object.get_plugin_type() == image.engine:
                continue

            plugin.plugin_object.stop_instance(image.id)

    def close(self):
        """
        Will clean up the VALManager.
        At first it will remove the capability from the capability engine and afterwards all the ``deactivate`` method
        for each plugin will be executed.
        """

        for plugin in self.plugin_manager.getAllPlugins():
            self.capability_repository.remove(capability=plugin.plugin_object.get_plugin_type())
            plugin.plugin_object.deactivate()
