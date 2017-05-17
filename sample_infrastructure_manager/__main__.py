import sys
import signal
from time import sleep
from registernodereceiver import RegisterNodeReceiver


new_node_publisher = RegisterNodeReceiver.Instance()


def signal_handler(signal, frame):
    new_node_publisher.stop()
    print('Server shutdown')
    sys.exit(0)


def main():
    new_node_publisher.start()

    while True:
        print("ok")
        sleep(1)


signal.signal(signal.SIGINT, signal_handler)
main()
