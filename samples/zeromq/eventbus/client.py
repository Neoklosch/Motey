import threading
import zmq
from time import sleep


class Client(object):
    context = None
    subscriber = None
    publisher = None

    def __init__(self, name, sleep_time):
        self.send_thread = threading.Thread(target=self.send, args=())
        self.receive_thread = threading.Thread(target=self.receive, args=())
        self.send_thread.daemon = True
        self.receive_thread.daemon = True

        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.publisher = self.context.socket(zmq.PUB)
        self.stopped = False
        self.name = name
        self.sleep_time = sleep_time

    def start(self):
        print("start %s" % self.name)
        self.publisher.connect('tcp://localhost:5235')
        self.subscriber.connect('tcp://localhost:5234')
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, 'nodes')

        self.receive_thread.start()
        self.send_thread.start()

    def send(self):
        while not self.stopped:
            sleep(self.sleep_time)
            print("%s: will send > nodes#%s" % (self.name, self.name))
            self.publisher.send_string('nodes#%s' % self.name)

    def receive(self):
        while not self.stopped:
            result = self.subscriber.recv_string()
            topic, output = result.split('#', 1)
            print("%s: received: %s " % (self.name, output))


    def stop(self):
        self.stopped = True
