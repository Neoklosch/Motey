import threading
import paho.mqtt.client as mqtt
from prototype.decorators.singleton import Singleton
from prototype.configuration.configreader import config
from prototype.utils.logger import Logger


@Singleton
class MQTTServer(threading.Thread):
    ROUTES = {
        'blueprint': 'fog_node/blueprint',
        'capabilities': 'fog_node/capabilities',
        'nodestatus': 'fog_node/nodestatus',
    }

    def __init__(self):
        super().__init__()
        self.logger = Logger.Instance()
        self.client = mqtt.Client()
        self.client.username_pw_set(config['MQTT']['username'], config['MQTT']['password'])
        self.client.on_connect = self.handle_on_connect
        self.client.on_subscribe = self.handle_on_subscribe
        self.register_routes()
        self.client.on_unsubscribe = self.handle_on_unsubscribe
        self.client.on_disconnect = self.handle_on_disconnect

    def register_routes(self):
        self.client.message_callback_add(self.ROUTES['blueprint'], self.handle_blueprints)
        self.client.message_callback_add(self.ROUTES['capabilities'], self.handle_capabilities)
        self.client.message_callback_add(self.ROUTES['nodestatus'], self.handle_node_status)

    def run(self):
        try:
            self.client.connect(host=config['MQTT']['ip'], port=int(config['MQTT']['port']), keepalive=int(config['MQTT']['keepalive']))
            self.client.loop_forever()
        except OSError:
            self.logger.error('MQTT server not available')

    def stop(self):
        self.client.loop_stop()

    def handle_on_connect(self, client, userdata, flags, resultcode):
        """
        The value of rc indicates success or not:
            0: Connection successful
            1: Connection refused - incorrect protocol version
            2: Connection refused - invalid client identifier
            3: Connection refused - server unavailable
            4: Connection refused - bad username or password
            5: Connection refused - not authorised
            6-255: Currently unused.
        """

        if resultcode is not 0:
            self.logger.info("Can not connect")
        else:
            self.logger.info("Connected: " + str(resultcode))
            client.subscribe(self.ROUTES['blueprint'])
            client.subscribe(self.ROUTES['capabilities'])
            client.subscribe(self.ROUTES['nodestatus'])

    def handle_on_subscribe(self, client, userdata, mid, granted_qos):
        self.logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))

    def handle_blueprints(self, client, userdata, message):
        print('%s %s' % (message.topic, str(message.payload)))

    def handle_capabilities(self, client, userdata, message):
        print('%s %s' % (message.topic, str(message.payload)))

    def handle_node_status(self, client, userdata, message):
        print('%s %s' % (message.topic, str(message.payload)))

    def handle_on_unsubscribe(self, client, userdata, mid):
        self.logger.info("Unsubscribed: " + str(mid))

    def handle_on_disconnect(self, client, userdata, resultcode):
        self.logger.info("Disconnected: " + str(resultcode))
