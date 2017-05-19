import threading

import zmq
from databasemanager import DatabaseManager
from decorators.singleton import Singleton
from newnodepublisher import NewNodePublisher


@Singleton
class RegisterNodeReceiver(threading.Thread):
    context = None
    receiver = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.context = zmq.Context()
        self.receiver = self.context.socket(zmq.REP)
        self.database_manager = DatabaseManager.Instance()
        self.new_node_publisher = NewNodePublisher.Instance()
        self.stopped = True

    def run(self):
        self.receiver.bind('tcp://*:5234')
        self.new_node_publisher.start()
        self.stopped = False
        while not self.stopped:
            print("enter the loop")
            new_ip = self.receiver.recv_string()
            print('New node ip: %s' % new_ip)
            self.database_manager.add_node(new_ip)

            self.new_node_publisher.publish(self.database_manager.get_all_nodes())

            self.receiver.send_string('ok')

    def stop(self):
        self.stopped = True
        self.new_node_publisher.stop()
