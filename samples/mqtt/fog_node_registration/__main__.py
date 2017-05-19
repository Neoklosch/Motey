import signal
import sys
from time import sleep

from newnodesubscriber import NewNodeSubscriber

new_node_subscriber = NewNodeSubscriber.Instance()


def signal_handler(signal, frame):
    new_node_subscriber.stop()
    print('Server shutdown')
    sys.exit(0)


def main():
    new_node_subscriber.start()

    while True:
        print("do something")
        new_node_subscriber.send_ip()
        sleep(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
