import threading
from time import sleep

import paho.mqtt.client as mqtt

counter = 0
stopped = False
topic = 'receive_nodes'
iterations = 1000
qos_level = 2


def run_client():
    client.loop_forever()


run_server_thread = threading.Thread(target=run_client, args=())
run_server_thread.daemon = True

client = mqtt.Client()
client.username_pw_set('test', 'test')
client.connect(host='172.18.0.3', port=1883)
run_server_thread.start()

for index in range(iterations):
    client.publish(topic=topic, payload='192.168.0.%s' % index, qos=qos_level)

while True:
    sleep(.1)
