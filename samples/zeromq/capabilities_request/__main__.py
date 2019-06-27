import signal
import sys
import threading
from time import sleep

import zmq

context = zmq.Context()
client = context.socket(zmq.REQ)


def signal_handler(signal, frame):
    print('shutdown')
    sys.exit(0)


def main():
    client.connect("tcp://172.18.0.11:5091")

    client.send_string("")

    #  Get the reply.
    message = client.recv_string()
    print("Received reply %s [ %s ]" % (1, message))


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
