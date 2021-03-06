import threading

import paho.mqtt.client as mqtt


class MQTTServer(object):
    """
    MQTT server to register and unregister adjacent fog nodes.
    The webserver runs in a separate thread and will not block the main thread.
    """

    def __init__(self, logger, nodes_repository, host='127.0.0.1', port=1883, username=None, password=None,
                 keepalive=60):
        """
        Constructor ot the MQTT server.

        :param logger: DI injected
        :type logger: motey.utils.logger.Logger
        :param nodes_repository: DI injected
        :type nodes_repository: motey.repositories.nodes_repository.NodesRepository
        :param host: The host of the MQTT broker. Default is ``'127.0.0.1'``.
        :param port: The port of the MQTT broker. Default is ``1883``.
        :param username: Username to authenticate on the MQTT broker. Default is None.
        :param password: Password to authenticate on the MQTT broker. Default is None.
        :param keepalive: Maximum period in seconds between communications with the
        broker. If no other messages are being exchanged, this controls the
        rate at which the client will send ping messages to the broker.
        """

        # Routes for registering and unregistering nodes
        self.ROUTES = {
            'register_node': {
                'topic': 'motey/v1/register',
                'callback': self.handle_register_node
            },
            'remove_node': {
                'topic': 'motey/v1/remove',
                'callback': self.handle_nodes_removal
            },
            'nodes_request': {
                'topic': 'motey/v1/nodes_request',
                'callback': self.handle_nodes_request
            },
        }

        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.username = username
        self.password = password
        self.logger = logger
        self.nodes_repository = nodes_repository
        self.client = mqtt.Client()
        if username and password:
            self.client.username_pw_set(username=self.username, password=self.password)
        self.client.on_connect = self.handle_on_connect
        self.register_routes()
        self.client.on_disconnect = self.handle_on_disconnect
        self._after_connect = None
        self.nodes_request_callback = None
        self.run_server_thread = threading.Thread(target=self.run_server, args=())
        self.run_server_thread.daemon = True

    @property
    def after_connect(self):
        return self._after_connect

    @after_connect.setter
    def after_connect(self, handler):
        self._after_connect = handler

    def register_routes(self):
        """
        Adds all the configured MQTT endpoints.
        """
        for key, value in self.ROUTES.items():
            if value['callback']:
                self.client.message_callback_add(sub=value['topic'], callback=value['callback'])

    def start(self):
        """
       Starts the execution thread.
       """
        self.run_server_thread.start()

    def run_server(self):
        """
        Starts the server and add an info to the logs, that the MQTT server is started.
        Also adds an error message to the logs if the broker is not available.
        """
        try:
            self.client.connect(host=self.host, port=self.port, keepalive=self.keepalive)
            self.logger.info('MQTT server started')
            self.client.loop_forever()
        except OSError:
            self.logger.error('MQTT broker is not available')

    def stop(self):
        """
        Stops the MQTT server and add an info the logs, that the server is stopped.
        """
        self.client.loop_stop()
        self.logger.info('MQTT server stopped')

    def publish_new_node(self, ip=None):
        """
        Publish the info that a new node is available to the all subscribers.
        If the ``ip`` is none, nothing will be send.

        :param ip: The IP address of the new node. Default is None.
        """
        if ip:
            self.client.publish(topic=self.ROUTES['register_node']['topic'], payload=ip)

    def publish_node_request(self, ip=None):
        """
        Publish the request to fetch the ip from all existing nodes.

        :param ip: the own ip to let the other nodes know where the request cames from.
        """
        if ip:
            self.client.publish(topic=self.ROUTES['nodes_request']['topic'], payload=ip)

    def remove_node(self, ip=None):
        """
        Remove a specific node and publish it to all subscribers.
        If the ``ip`` is none, nothing will be send.

        :param ip: The IP address of the new node. Default is None.
        """
        if ip:
            self.client.publish(topic=self.ROUTES['remove_node']['topic'], payload=ip)

    def handle_on_connect(self, client, userdata, flags, resultcode):
        """
        Define the connect callback implementation.
        If the client is connected to the MQTT broker, the nodes will be registered and the ``_after_connect`` method
        will be executed.

        flags is a dict that contains response flags from the broker:
            flags['session present'] - this flag is useful for clients that are
                using clean session set to 0 only. If a client with clean
                session=0, that reconnects to a broker that it has previously
                connected to, this flag indicates whether the broker still has the
                session information for the client. If 1, the session still exists.

        The value of rc indicates success or not:
            0: Connection successful
            1: Connection refused - incorrect protocol version
            2: Connection refused - invalid client identifier
            3: Connection refused - server unavailable
            4: Connection refused - bad username or password
            5: Connection refused - not authorised
            6-255: Currently unused.

        :param client:     the client instance for this callback
        :param userdata:   the private user data as set in Client() or userdata_set()
        :param flags:      response flags sent by the broker
        :param resultcode: the connection result
        """

        if resultcode is not 0:
            self.logger.info("Connection to the broker failed")
        else:
            for key, value in self.ROUTES.items():
                client.subscribe(topic=value['topic'])
        if self._after_connect:
            self._after_connect()

    def handle_nodes_request(self, client, userdata, message):
        """
        Define the node request callback implementation.
        Will execute the callback of the request to fetch the ip from all existing nodes.

        :param client:     the client instance for this callback
        :param userdata:   the private user data as set in Client() or userdata_set()
        :param message:    the data which was send
        """
        if self.nodes_request_callback:
            self.nodes_request_callback(client, userdata, message)

    def handle_nodes_removal(self, client, userdata, message):
        pass

    def handle_register_node(self, client, userdata, message):
        """
        Define the register new node callback implementation.
        Adds the new node to the ``NodesRepository``.

        :param client:     the client instance for this callback
        :param userdata:   the private user data as set in Client() or userdata_set()
        :param message:    the data which was send
                """
        new_node = message.payload.decode('utf-8')
        self.nodes_repository.add(ip=new_node)

    def handle_on_disconnect(self, client, userdata, resultcode):
        """
        Define the disconnect callback implementation.

        :param client:     the client instance for this callback
        :param userdata:   the private user data as set in Client() or userdata_set()
        :param resultcode: the connection result
        """
        self.logger.info("Disconnected from MQTT broker " + str(resultcode))
