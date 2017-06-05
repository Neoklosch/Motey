import signal
import sys
import threading
from time import sleep

import zmq

context = zmq.Context()
server = context.socket(zmq.REP)
client = context.socket(zmq.REQ)


def signal_handler(signal, frame):
    print('shutdown')
    sys.exit(0)


def main():
    server.bind("tcp://*:5555")

    server_thread = threading.Thread(target=start_server, args=())
    server_thread.daemon = True
    server_thread.start()

    client.connect("tcp://localhost:5555")

    for request in range(10):
        print("Sending request %s" % request)
        client.send_string("Hello ")

        #  Get the reply.
        message = client.recv_string()
        print("Received reply %s [ %s ]" % (request, message))


def start_server():
    while True:
        #  Wait for next request from client
        message = server.recv_string()
        print("Received request: %s" % message)

        #  Do some 'work'
        sleep(1)

        #  Send reply back to client
        server.send_string("World")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
