from motey.utils import network_utils
from rx.subjects import Subject


class CommunicationManager(object):
    capability_event_stream = Subject()

    def __init__(self, api_server, mqtt_server, zeromq_server):
        self.api_server = api_server
        self.mqtt_server = mqtt_server
        self.zeromq_server = zeromq_server

        self.mqtt_server.after_connect = self.after_connect_callback
        self.mqtt_server.nodes_request_callback = self.__nodes_request_callback

    @property
    def after_capabilities_request(self):
        return self.zeromq_server.after_capabilities_request_handler

    @after_capabilities_request.setter
    def after_capabilities_request(self, handler):
        self.zeromq_server.after_capabilities_request_handler = handler

    def start(self):
        self.api_server.start()
        self.mqtt_server.start()
        self.zeromq_server.start()

    def stop(self):
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
        return self.zeromq_server.deploy_image(image)

    def request_image_status(self, image):
        return self.zeromq_server.request_image_status(image)

    def request_capabilities(self, node):
        return self.zeromq_server.request_capabilities(node)

    def terminate_image(self, image):
        self.zeromq_server.terminate_image(image)
