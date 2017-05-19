import threading

import zmq
from decorators.singleton import Singleton


@Singleton
class NewNodeSubscriber(threading.Thread):
    context = None
    subscriber = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.stopped = True

    def run(self):
        self.subscriber.connect('tcp://localhost:5235')
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, 'nodes')

        self.stopped = False
        while not self.stopped:
            print('loop to get the json')
            result = self.subscriber.recv_string()
            topic, json_result = result.split('#', 1)
            print("broadcast received: %s " % json_result)

    def stop(self):
        self.stopped = True
