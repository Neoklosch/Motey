import signal
import sys
from time import sleep
from registernodereceiver import RegisterNodeReceiver


new_node_receiver = RegisterNodeReceiver.Instance()


def signal_handler(signal, frame):
    new_node_receiver.stop()
    print('Server shutdown')
    sys.exit(0)


def main():
    new_node_receiver.start()

    while True:
        print("ok")
        sleep(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
