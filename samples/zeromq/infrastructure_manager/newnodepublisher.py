import threading
from time import sleep

import zmq
from databasemanager import DatabaseManager
from decorators.singleton import Singleton


@Singleton
class NewNodePublisher(threading.Thread):
    context = None
    publisher = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.database_manager = DatabaseManager.Instance()

    def run(self):
        self.publisher.bind('tcp://*:5235')
        print('NewNodePublisher started')
        while True:
            sleep(1)

    def stop(self):
        pass

    def publish(self, message):
        print('publish: %s' % message)
        what = self.publisher.send_string('nodes#%s' % message)
        print(what)
