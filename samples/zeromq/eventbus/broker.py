import threading
import zmq
import zmq.asyncio
from time import sleep


class EventBusBroker(threading.Thread):
    context = None
    subscriber = None
    publisher = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.publisher = self.context.socket(zmq.PUB)
        self.stopped = False

    def run(self):
        self.publisher.bind('tcp://*:5234')
        self.subscriber.bind('tcp://*:5235')
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, 'nodes')

        self.doit()
        while not self.stopped:
            sleep(1)

    def doit(self):
        while not self.stopped:
            result = self.subscriber.recv_string()
            topic, output = result.split('#', 1)
            print("Broker: received: %s " % output)
            self.publisher.send_string('nodes#%s' % output)

    def stop(self):
        self.stopped = True
