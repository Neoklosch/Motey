import json
import threading

import zmq

from motey.configuration.configreader import config
from motey.database.labeling_database import LabelingDatabase
from motey.decorators.singleton import Singleton


@Singleton
class LabelingEngine(object):
    """
    This module provides a connection endpoint for the hardware layer.
    New labels can be added via a ZeroMQ tcp publisher.
    The port can be configured in the config.ini file.
    This class is implemented as a Singleton and should be called via HardwareEventEngine.Instance().

    """

    # the socket of the subscriber
    subscriber = None

    def __init__(self):
        self.labeling_database = LabelingDatabase.Instance()
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.receiver_thread = threading.Thread(target=self.__run_receiver_thread, args=())
        self.receiver_thread.daemon = True
        self.stopped = False

    def start(self):
        """
        Starts the listening on a given port.
        This method will be executed on a separate thread.

        """
        self.subscriber.bind('tcp://*:%s' % config['LABELINGENGINE']['port'])
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, 'labelingevent')
        self.receiver_thread.start()

    def __run_receiver_thread(self):
        """
        Private function which is be executed after the start method is called.
        The method will wait for an event where it is subscribed on.
        After receiving an event a new label will be added to the LabelingDatabase.

        """
        while not self.stopped:
            result = self.subscriber.recv_string()
            topic, output = result.split('#', 1)
            try:
                json_result = json.loads(output)
                if isinstance(json_result, list):
                    for entry in json_result:
                        self.__add_label(entry)
                elif isinstance(json_result, dict):
                    self.__add_label(json_result)
            except (TypeError, json.JSONDecodeError):
                pass

    def __add_label(self, entry):
        if 'label' in entry and 'label_type' in entry:
            self.labeling_database.add(label=entry['label'], label_type=entry['label_type'])
