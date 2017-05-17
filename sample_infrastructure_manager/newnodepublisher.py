import threading
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
        self.publisher.bind('tcp://127.0.0.1:5235')
        print('NewNodePublisher started')

    def stop(self):
        pass

    def publish(self, message):
        self.publisher.send_json(message)
