import json
import threading

import zmq

from motey.configuration.configreader import config
from motey.database.labeling_database import LabelingDatabase
from motey.decorators.singleton import Singleton
from motey.utils.logger import Logger


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
        self.logger = Logger.Instance()
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
        self.logger.info('labeling engine started')

    def stop(self):
        self.logger.info('labeling engine stopped')

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
                        self.__perform_label_action(entry)
                elif isinstance(json_result, dict):
                    self.__perform_label_action(json_result)
            except (TypeError, json.JSONDecodeError):
                pass

    def __perform_label_action(self, entry):
        """
        Perform a specific action for the given entry.
        Possible action types are `add` and `remove`.
        :param entry: the label entry which should be used to perform the action

        """
        if 'action' in entry and 'label' in entry and 'label_type' in entry:
            if entry['action'] == 'add':
                self.labeling_database.add(label=entry['label'], label_type=entry['label_type'])
            elif entry['action'] == 'remove':
                self.labeling_database.remove(label=entry['label'], label_type=entry['label_type'])
            else:
                self.logger.warning('Unknown labeling action: %s' % entry['action'])
