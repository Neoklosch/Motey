import docker
from docker.errors import APIError, NotFound, ContainerError, ImageNotFound

import motey.val.plugins.abstractVAL as abstractVAL
from motey.configuration.configreader import config
from motey.models.image_state import ImageState
from motey.models.systemstatus import SystemStatus
from motey.models.valinstancestatus import VALInstanceStatus


class DockerVAL(abstractVAL.AbstractVAL):
    """
    Concrete implementation of the docker virtualization abstraction layer (VAL).
    """

    def __init__(self):
        """
        Constructor of the DockerVAL.

        """
        super().__init__()

    def get_docker_client(self):
        """
        Instantiates the docker client.

        :return: the docker client
        """
        return docker.DockerClient(base_url=config['DOCKER']['url'])

    def get_plugin_type(self):
        """
        Returns the specific plugin type.

        :return: the specific plugin type.
        """
        return 'docker'

    def has_image(self, image_name):
        """
        Checks if an specific images exists.

        :param image_name: the name of the image to search for. Can be the ``image.id`` or the ``image.short_id``.
        :return: True if the image exist, otherwise False.
        """
        client = self.get_docker_client()
        images = []
        try:
            images = client.images.list()
        except APIError as apie:
            return False

        for image in client.images.list():
            if image.id == image_name or image.short_id == image_name or image.id == 'sha256:%s' % image_name or image.short_id == 'sha256:%s' % image_name:
                return True
        return False

    def load_image(self, image_name):
        """
        Load the image to the device, but does not start the image himself.
        It is a wrapper around the ``docker.images.pull`` command.

        :param image_name: the image to be loaded.
        """
        client = self.get_docker_client()
        try:
            client.images.pull(image_name)
        except APIError as apie:
            pass

    def delete_image(self, image_name):
        """
        Delete an image, but not the instance of it.
        It is a wrapper around the ``docker.images.remove`` command.

        :param image_name: the image to be deleted.
        """
        client = self.get_docker_client()
        try:
            client.images.remove(image_name)
        except ContainerError as ce:
            pass
        except ImageNotFound as inf:
            pass
        except APIError as apie:
            pass

    def create_instance(self, image_name, parameters={}):
        """
        Create and start an instance of an image.
        It is a wrapper around the ``docker.containers.create`` command.

        :param image_name: the name of the image which should be created
        :param parameters: execution parameters. Same as in the ``docker.create_container``.
        :return: the id of the created instance
        """
        container_id = None
        client = self.get_docker_client()
        try:
            if 'detach' in parameters:
                parameters.pop('detach')
                container = client.containers.create(image_name, detach=True, **parameters)
        except ContainerError as ce:
            if self.logger:
                self.logger.error("create docker instance > container could not be created")
        except ImageNotFound as inf:
            if self.logger:
                self.logger.error("create docker instance > image not found")
        except APIError as apie:
            if self.logger:
                self.logger.error("create docker instance > api error")
        return container_id

    def start_instance(self, instance_name, parameters={}):
        """
        Start an existing image instance.
        It is a wrapper around the ``docker.containers.run`` command.

        :param instance_name: the name of the existing instance
        :param parameters: execution parameters. Same as in the ``docker.create_container``.
        :return: the id of the started instance
        """
        container_id = None
        client = self.get_docker_client()
        try:
            if 'detach' in parameters:
                parameters.pop('detach')
            container = client.containers.run(instance_name, detach=True, **parameters)
            container_id = container.id
        except ContainerError as ce:
            if self.logger:
                self.logger.error("start docker instance > container could not be created")
        except ImageNotFound as inf:
            if self.logger:
                self.logger.error("start docker instance > image not found")
        except APIError as apie:
            if self.logger:
                self.logger.error("start docker instance > api error")
        return container_id

    def stop_instance(self, container_name):
        """
        Stop an existing image instance.
        It is a wrapper around the ``docker.containers.stop`` command.

        :param container_name: the name of the container to be stopped
        """
        client = self.get_docker_client()
        try:
            client.containers.stop(container_name)
        except ContainerError as ce:
            pass
        except ImageNotFound as inf:
            pass
        except APIError as apie:
            pass

    def has_instance(self, container_name):
        """
        Checks if an image instance exists.
        It is a wrapper around the ``docker.containers.get`` command.

        :param container_name: the name of an existing instance
        """
        client = self.get_docker_client()
        try:
            client.containers.get(container_name)
        except (NotFound, APIError):
            return False
        return True

    def get_all_running_instances(self):
        """
        Returns a list with all running instance in this VAL.
        It is a wrapper around the ``docker.containers.list(filters={'status': 'running'})`` command.

        :return: list of instances
        """
        client = self.get_docker_client()
        return client.containers.list(filters={'status': 'running'})

    def get_image_instance_state(self, container_name):
        client = self.get_docker_client()
        image_status = None
        try:
            container = client.containers.get(container_name)
            status = container.attrs['State']['Status']
            if status == 'created':
                image_status = ImageState.INSTANTIATING
            if status == 'restarting':
                image_status = ImageState.INSTANTIATING
            elif status == 'running':
                image_status = ImageState.RUNNING
            elif status == 'paused':
                image_status = ImageState.STOPPING
            elif status == 'removing':
                image_status = ImageState.STOPPING
            elif status == 'exited':
                image_status = ImageState.TERMINATED
            elif status == 'dead':
                image_status = ImageState.TERMINATED
            else:
                image_status = ImageState.ERROR
        except (NotFound, APIError):
            image_status = ImageState.ERROR

    def get_stats(self, container_name):
        """
        Returns object which is type of ``Status``. Represents the status of a container.

        :param container_name: the name of the container
        :return: object from type ``Status``
        """
        client = self.get_docker_client()
        status = VALInstanceStatus()
        try:
            container = client.containers.get(container_name)
            service_stats = container.stats(decode=True, stream=False)
            status.image_name = container.attrs['Name']
            status.image = container.attrs['Image']
            status.status = container.attrs['State']['Status']
            status.created_at = container.attrs['Created']
            status.ip = container.attrs['NetworkSettings']['IPAddress']
            status.used_memory = service_stats['memory_stats']['usage']
            status.used_cpu = service_stats['cpu_stats']['cpu_usage']['total_usage']
            status.network_tx_bytes = service_stats['networks']['eth0']['tx_bytes']
            status.network_rx_bytes = service_stats['networks']['eth0']['rx_bytes']
        except (NotFound, APIError):
            return None
        return status

    def get_all_instances_stats(self):
        """
        Returns object which is type of ``Status``. Represents the status of all docker container.

        :return: object from type ``Status``
        """
        client = self.get_docker_client()
        system_status = SystemStatus()
        for instance in self.get_all_running_instances():
            container = client.containers.get(instance.id)
            service_stats = container.stats(decode=True, stream=False)
            system_status.used_memory += int(service_stats['memory_stats']['usage'])
            system_status.used_cpu += int(service_stats['cpu_stats']['cpu_usage']['total_usage'])
            system_status.network_tx_bytes += int(service_stats['networks']['eth0']['tx_bytes'])
            system_status.network_rx_bytes += int(service_stats['networks']['eth0']['rx_bytes'])

        return system_status
