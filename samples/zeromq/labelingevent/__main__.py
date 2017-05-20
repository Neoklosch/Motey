import signal
import sys
from time import sleep
import threading
from time import sleep
import json

import zmq


context = zmq.Context()
publisher = context.socket(zmq.PUB)
count = 0


def signal_handler(signal, frame):
    print('shutdown')
    sys.exit(0)


def publish_data():
    global count
    while True:
        sleep(2)

        json_data = [{'label': 'zigbee%s' % count, 'label_type': 'labelingevent'}, {'label': 'wifi%s' % count, 'label_type': 'labelingevent'}]
        print('will send > labelingevent#%s' % json.dumps(json_data))
        publisher.send_string('labelingevent#%s' % json.dumps(json_data))
        count = count + 1


def main():
    publisher.connect('tcp://localhost:5090')
    send_thread = threading.Thread(target=publish_data, args=())
    send_thread.start()

    while True:
        sleep(.1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
