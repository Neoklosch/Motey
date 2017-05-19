import threading

import zmq

from motey.database.labeling_database import LabelingDatabase
from motey.decorators.singleton import Singleton
from motey.configuration.configreader import config


@Singleton
class HardwareEventEngine(object):
    subscriber = None

    def __init__(self):
        self.labeling_engine = LabelingDatabase.Instance()
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.receiver_thread = threading.Thread(target=self.run_receiver_thread, args=())
        self.receiver_thread.daemon = True
        self.stopped = False

    def start(self):
        self.subscriber.bind('tcp://*:%s' % config['HARDWAREEVENT']['port'])
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, 'hardwareevent')
        self.receiver_thread.start()

    def run_receiver_thread(self):
        while not self.stopped:
            result = self.subscriber.recv_string()
            topic, output = result.split('#', 1)
            self.labeling_engine.add(label=output, label_type='hardwareevent')
