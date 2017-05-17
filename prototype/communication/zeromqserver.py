import threading
import zmq
from prototype.decorators.singleton import Singleton
from prototype.configuration.configreader import config
from prototype.utils.logger import Logger

@Singleton
class MQTTServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.logger = Logger.Instance()
        self.zero_mq_context = zmq.Context()
        self.sock = None
        self.stopped = True

    def run(self):
        self.sock = self.zero_mq_context.socket(zmq.REP)
        self.sock.bind("%s:%s" % (config['ZEROMQ']['url'], config['ZEROMQ']['port']))
        self.stopped = False
        while not self.stopped:
            message = self.sock.recv()
            print("ZeroMQ received: " + message)

    def stop(self):
        self.sock.close()