import threading
import zmq
from time import sleep
from decorators.singleton import Singleton


@Singleton
class NewNodeRegister(threading.Thread):
    context = None
    sender = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.context = zmq.Context()
        self.sender = self.context.socket(zmq.REQ)

    def run(self):
        self.sender.connect('tcp://localhost:5234')

        #  Do 10 requests, waiting each time for a response
        for index in range(10):
            print('Sending request with message: 192.168.0.%s' % index)
            self.sender.send_string('192.168.0.%s' % index)

            #  Get the reply.
            message = self.sender.recv()
            print('Received %s' % message)
            sleep(3)

    def stop(self):
        pass
