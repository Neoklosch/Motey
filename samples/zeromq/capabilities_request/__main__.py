import signal
import sys
from time import sleep
import threading
from time import sleep
import json

import zmq


context = zmq.Context()
publisher = context.socket(zmq.REQ)
count = 0


def signal_handler(signal, frame):
    print('shutdown')
    sys.exit(0)


def main():
    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to hello world server")
    publisher.connect("tcp://localhost:5091")

    publisher.send_string("a")

    #  Get the reply.
    message = publisher.recv_string()
    print("Received reply %s" % message)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
