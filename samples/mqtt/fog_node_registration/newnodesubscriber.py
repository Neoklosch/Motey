import json
import threading
import paho.mqtt.client as mqtt
from time import sleep
from decorators.singleton import Singleton


@Singleton
class NewNodeSubscriber(threading.Thread):
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

    def register_routes(self):
        self.client.message_callback_add('receive_nodes', self.handle_receive_nodes)

    def run(self):
        try:
            self.client.connect(host='172.17.0.3', port=1883)
            self.client.loop_forever()
        except OSError:
            print('MQTT server not available')

    def send_ip(self):
        for index in range(10):
            print('Sending request with message: 192.168.0.%s' % index)
            self.client.publish('register_node', '192.168.0.%s' % index)
            sleep(3)

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
            client.subscribe('receive_nodes')

    def handle_on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def handle_receive_nodes(self, client, userdata, message):
        print('%s %s' % (message.topic, str(message.payload)))
        json_payload = json.loads(message.payload.decode('utf-8'))
        print('%s %s' % (message.topic, str(json_payload)))

    def handle_on_unsubscribe(self, client, userdata, mid):
        print("Unsubscribed: " + str(mid))

    def handle_on_disconnect(self, client, userdata, resultcode):
        print("Disconnected: " + str(resultcode))
