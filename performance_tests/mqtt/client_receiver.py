import datetime
import threading
from time import sleep

import paho.mqtt.client as mqtt

counter = 0
topic = 'receive_nodes'
iterations = 1000
qos_level = 2


def handle_on_connect(client, userdata, flags, resultcode):
    if resultcode is 0:
        client.subscribe(topic=topic, qos=qos_level)


def handle_receive_nodes(client, userdata, message):
    global counter, receive_start_time
    if counter == 0:
        receive_start_time = datetime.datetime.now()
    result = message.payload.decode('utf-8')
    counter = counter + 1
    print(counter)
    if counter == iterations:
        delta = datetime.datetime.now() - receive_start_time
        print('Delta of receive loop: %s' % delta)
        client.disconnect()


def run_client():
    client.loop_forever()


run_server_thread = threading.Thread(target=run_client, args=())
run_server_thread.daemon = True

client = mqtt.Client()
client.username_pw_set('test', 'test')
client.on_connect = handle_on_connect
client.message_callback_add(sub=topic, callback=handle_receive_nodes)
client.connect(host='172.18.0.3', port=1883)
client.loop_forever()
