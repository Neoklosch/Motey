from yapsy.IPlugin import IPlugin

from motey.di.app_module import DICore


class AbstractVAL(IPlugin):
    """
    An abstract implementation for a virtualization abstraction layer (VAL).
    Should be inherited to build an custom VAL plugin.
    A VAL plugin is implemented as an yapsy plugin.
    Each plugin must be configured via a yapsy-plugin file.
    See more at http://yapsy.sourceforge.net/
    """

    def __init__(self):
        """
        Constructor of the AbstractVAL.
        """
        super().__init__()
        self.logger = DICore.logger()

    def get_plugin_type(self):
        """
        Returns the specific plugin type.

        :return: the specific plugin type.
        """
        raise NotImplementedError("Should have implemented this")

    def has_image(self, image_name):
        """
        Checks if an specific images exists.

        :param image_name: the name of the image to search for.
        :return: True if the image exist, otherwise False.
        """
        raise NotImplementedError("Should have implemented this")

    def load_image(self, image_name):
        """
        Load the image to the device, but does not start the image himself.

        :param image_name: the image to be loaded.
        """
        raise NotImplementedError("Should have implemented this")

    def delete_image(self, image_name):
        """
        Delete an image, but not the instance of it.

        :param image_name: the image to be deleted.
        """
        raise NotImplementedError("Should have implemented this")

    def create_instance(self, image_name, parameters={}):
        """
        Create and start an instance of an image.

        :param image_name: the name of the image which should be created
        :param parameters: execution parameters
        :return: the id of the created instance
        """
        raise NotImplementedError("Should have implemented this")

    def start_instance(self, instance_name, parameters={}):
        """
        Start an existing image instance.

        :param instance_name: the name of the existing instance
        :param parameters: execution parameters
        :return: should return the id of the started instance
        """
        raise NotImplementedError("Should have implemented this")

    def stop_instance(self, instance_name):
        """
        Stop an existing image instance.

        :param instance_name: the name of the container to be stopped
        """
        raise NotImplementedError("Should have implemented this")

    def has_instance(self, instance_name):
        """
        Checks if an image instance exists.

        :param instance_name: the name of an existing instance
        """
        raise NotImplementedError("Should have implemented this")

    def get_all_running_instances(self):
        """
        Returns a list with all running instance in this VAL.

        :return: list of instances
        """
        raise NotImplementedError("Should have implemented this")

    def get_stats(self, instance_name):
        """
        Returns object which is type of ``Status``. Represents the status of an instance.

        :param instance_name: the name of the instance
        :return: object from type ``Status``
        """
        raise NotImplementedError("Should have implemented this")

    def get_all_instances_stats(self):
        """
        Returns object which is type of ``Status``. Represents the status of all instances of this plugin type.

        :return: object from type ``Status``
        """
        raise NotImplementedError("Should have implemented this")

    def activate(self):
        """
        Called at plugin activation.
        """
        self.logger.info("%s plugin activated" % self.get_plugin_type())

    def deactivate(self):
        """
        Called when the plugin is disabled.
        """
        self.logger.info("%s plugin deactivated" % self.get_plugin_type())
