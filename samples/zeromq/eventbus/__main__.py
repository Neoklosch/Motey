import signal
import sys
from time import sleep

from broker import EventBusBroker
from client import Client

broker = EventBusBroker()
client_one = Client('ClientOne', 3)
client_two = Client('ClientTwo', 5)
client_three = Client('ClientThree', 7)


def signal_handler(signal, frame):
    client_one.stop()
    client_two.stop()
    client_three.stop()
    broker.stop()
    print('Server shutdown')
    sys.exit(0)


def main():
    broker.start()
    client_one.start()
    client_two.start()
    client_three.start()

    while True:
        print("main do something")
        sleep(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
