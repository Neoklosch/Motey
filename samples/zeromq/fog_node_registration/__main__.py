import signal
import sys
from time import sleep
from newnoderegister import NewNodeRegister
from newnodesubscriber import NewNodeSubscriber


new_node_subscriber = NewNodeSubscriber.Instance()
new_node_register = NewNodeRegister.Instance()


def signal_handler(signal, frame):
    new_node_register.stop()
    new_node_subscriber.stop()
    print('Server shutdown')
    sys.exit(0)


def main():
    new_node_subscriber.start()
    new_node_register.start()

    while True:
        print("do something")
        sleep(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
