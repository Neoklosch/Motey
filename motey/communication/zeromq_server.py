from rx.subjects import Subject
import threading

import zmq

from motey.configuration.configreader import config


class ZeroMQServer(object):
    capability_event_stream = Subject()

    def __init__(self, logger):
        self.logger = logger
        self.context = zmq.Context()
        self.capabilities_subscriber = self.context.socket(zmq.SUB)
        self.capabilities_sender = self.context.socket(zmq.REP)

        self.capabilities_subscriber_thread = threading.Thread(target=self.__run_capabilities_subscriber_thread, args=())
        self.capabilities_subscriber_thread.daemon = True

        self.capabilities_sender_thread = threading.Thread(target=self.__run_capabilities_sender_thread, args=())
        self.capabilities_sender_thread.daemon = True
        self.stopped = False

    def start(self):
        """
        Starts the listening on a given port.
        This method will be executed on a separate thread.
        """

        self.capabilities_subscriber.bind('tcp://*:%s' % config['LABELINGENGINE']['port'])
        self.capabilities_subscriber.setsockopt_string(zmq.SUBSCRIBE, 'labelingevent')
        self.capabilities_subscriber_thread.start()

        self.capabilities_sender.bind('tcp://*:%s' % config['CAPABILITIES_SENDER']['port'])
        self.capabilities_sender_thread.start()

        self.logger.info('ZeroMQ server started')

    def stop(self):
        """
        Should be executed to clean up the labeling engine
        """

        self.logger.info('ZeroMQ server stopped')

    def __run_capabilities_subscriber_thread(self):
        """
        Private function which is be executed after the start method is called.
        The method will wait for an event where it is subscribed on.
        After receiving an event a new label will be added to the LabelingDatabase.
        """

        while not self.stopped:
            result = self.capabilities_subscriber.recv_string()
            topic, output = result.split('#', 1)
            self.capability_event_stream.on_next(output)

    def __run_capabilities_sender_thread(self):
        while not self.stopped:
            result = self.capabilities_sender.recv_string()
            topic, output = result.split('#', 1)
            # TODO: do somtething with output
            self.capabilities_sender.send_string('')

    def request_capabilities(self, ip):
        if not ip:
            return None
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://%s:%s" % (ip, config['CAPABILITIES_SENDER']['port']))
        socket.send_string("a")
        message = socket.recv()
        return message
