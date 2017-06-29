from motey.utils import network_utils


class CommunicationManager(object):
    """
    This class acts as an facade for the communication endpoints like the ``MQTT server``, the ``API server`` and the
    ``ZeroMQ server``.
    It covers all method calls and can start and stop the mentioned components.
    """

    def __init__(self, api_server, mqtt_server, zeromq_server):
        """
        Constructor of the class.

        :param api_server: DI injected.
        :type api_server: motey.communication.apiserver.APIServer
        :param mqtt_server: DI injected.
        :type mqtt_server: motey.communication.mqttserver.MQTTServer
        :param zeromq_server: DI injected.
        :type zeromq_server: motey.communication.zeromq_server.ZeroMQServer
        """
        self.api_server = api_server
        self.mqtt_server = mqtt_server
        self.zeromq_server = zeromq_server

        self.mqtt_server.after_connect = self.after_connect_callback
        self.mqtt_server.nodes_request_callback = self.__nodes_request_callback

        self.add_capability_event_stream = self.zeromq_server.add_capability_event_stream
        self.remove_capability_event_stream = self.zeromq_server.remove_capability_event_stream

    @property
    def after_capabilities_request(self):
        """
        Facades the ``ZeroMQServer.after_capabilities_request_handler()`` getter.
        Returns the handler which will be executed after a capability request was received.

        :return: the handler which will be executed after a capability request was received.
        """
        return self.zeromq_server.after_capabilities_request_handler

    @after_capabilities_request.setter
    def after_capabilities_request(self, handler):
        """
        Facades the ``ZeroMQServer.after_capabilities_request`` setter.
        Will set the handler which will be executed after a capability request was received.

        :param handler: the handler which will be executed after a capability request was received.
        """
        self.zeromq_server.after_capabilities_request_handler = handler

    def start(self):
        """
        Start all the connected communication components.
        """
        self.api_server.start()
        self.mqtt_server.start()
        self.zeromq_server.start()

    def stop(self):
        """
        Stop all the connected communication components.
        Will send out a mqtt message to remove the current node.
        """
        self.zeromq_server.stop()
        self.mqtt_server.remove_node(network_utils.get_own_ip())
        self.mqtt_server.stop()
        self.api_server.stop()

    def after_connect_callback(self):
        """
        Will be called after the MQTTServer has established a connection to the broker.
        Send out a request to fetch the ip from all existing nodes.
        """
        self.mqtt_server.publish_node_request(network_utils.get_own_ip())

    def __nodes_request_callback(self, client, userdata, message):
        """
        Will be called if a request to fetch the ip from all existing nodes comes in.
        Send out the ip of the node.

        :param client:     the client instance for this callback
        :param userdata:   the private user data as set in Client() or userdata_set()
        :param message:    the data which was send
        """
        self.mqtt_server.publish_new_node(network_utils.get_own_ip())

    def deploy_image(self, image):
        """
        Facades the ``ZeroMQServer.deploy_image()`` method.
        Will deploy an image to the node stored in the ``Image.node`` attribute.

        :param image: Image to be deployed.
        :type image: motey.models.image.Image
        :return: the id of the deployed image or None if something went wrong.
        """
        return self.zeromq_server.deploy_image(image)

    def request_image_status(self, image):
        """
        Facades the ``ZeroMQServer.request_image_status()`` method.
        Request the status of an specific image instance or None if something went wrong.

        :param image: Image to be used to get the status.
        :type image: motey.models.image.Image
        :return: the status of the image or None if something went wrong
        """
        return self.zeromq_server.request_image_status(image)

    def request_capabilities(self, ip):
        """
        Facades the ``ZeroMQServer.request_capabilities()`` method.
        Will fetch the capabilities of a specific node and will return them.

        :param ip: The ip of the node to be requested.
        :type ip: str
        :return: the capabilities of a specific node
        """
        return self.zeromq_server.request_capabilities(ip)

    def terminate_image(self, image):
        """
        Facades the ``ZeroMQServer.terminate_image()`` method.
        Will terminate an image instance.

        :param image: the image instance to be terminated
        :type image: motey.models.image.Image
        """
        self.zeromq_server.terminate_image(image)
