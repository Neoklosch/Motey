import json
import threading
import paho.mqtt.client as mqtt
from databasemanager import DatabaseManager
from decorators.singleton import Singleton


@Singleton
class RegisterNodeReceiver(threading.Thread):
    ROUTES = {
        'register_node': 'fog_node/register',
        'remove_node': 'fog_node/remove',
        'receive_nodes': 'fog_node/receive_nodes'
    }

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.client = mqtt.Client()
        self.client.username_pw_set('test', 'test')
        self.client.on_connect = self.handle_on_connect
        self.client.on_subscribe = self.handle_on_subscribe
        self.register_routes()
        self.client.on_unsubscribe = self.handle_on_unsubscribe
        self.client.on_disconnect = self.handle_on_disconnect
        self.database_manager = DatabaseManager.Instance()

    def register_routes(self):
        self.client.message_callback_add(sub=self.ROUTES['register_node'], callback=self.handle_register_node)
        self.client.message_callback_add(sub=self.ROUTES['remove_node'], callback=self.handle_remove_node)

    def run(self):
        try:
            self.client.connect(host='172.17.0.3', port=1883)
            self.client.loop_forever()
        except OSError:
            print('MQTT server not available')

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
            print("Can not connect")
        else:
            print("Connected: " + str(resultcode))
            client.subscribe(topic=self.ROUTES['register_node'])
            client.subscribe(topic=self.ROUTES['remove_node'])

    def handle_on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def handle_register_node(self, client, userdata, message):
        new_ip = message.payload.decode('utf-8')
        print('%s %s' % (message.topic, new_ip))
        self.database_manager.add_node(ip=new_ip)

        all_nodes = json.dumps(self.database_manager.get_all_nodes())
        print("I will send: %s" % all_nodes)
        self.client.publish(topic=self.ROUTES['receive_nodes'], payload=all_nodes)

    def handle_remove_node(self, client, userdata, message):
        ip_to_remove = message.payload.decode('utf-8')
        print('%s %s' % (message.topic, ip_to_remove))
        self.database_manager.remove_node(ip=ip_to_remove)

        all_nodes = json.dumps(self.database_manager.get_all_nodes())
        print("I will send: %s" % all_nodes)
        self.client.publish(topic=self.ROUTES['receive_nodes'], payload=all_nodes)

    def handle_on_unsubscribe(self, client, userdata, mid):
        print("Unsubscribed: " + str(mid))

    def handle_on_disconnect(self, client, userdata, resultcode):
        print("Disconnected: " + str(resultcode))
