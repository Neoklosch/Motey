import threading
import zmq
from fog_node_engine.decorators.singleton import Singleton
from fog_node_engine.configuration.configreader import config
from fog_node_engine.utils.logger import Logger


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
