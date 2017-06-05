import json
import threading

import zmq
from rx.subjects import Subject

from motey.configuration.configreader import config


class ZeroMQServer(object):
    """
    ZeroMQ server to communicate with adjacent fog nodes and to reply to requests.
    The different listeners will be executed in a separate thread and will not block the main thread.
    """

    capability_event_stream = Subject()

    def __init__(self, logger, valmanager):
        """
        Constructor ot the MQTT server.

        :param logger: DI injected
        :type logger: motey.utils.logger.Logger
        :param valmanager: DI injected
        :type valmanager: motey.val.valmanager.VALManager
        """
        self.logger = logger
        self.valmanager = valmanager
        self.context = zmq.Context()
        self.capabilities_subscriber = self.context.socket(zmq.SUB)
        self.capabilities_replier = self.context.socket(zmq.REP)
        self.deploy_image_replier = self.context.socket(zmq.REP)
        self.image_status_replier = self.context.socket(zmq.REP)
        self.image_terminate_replier = self.context.socket(zmq.REP)

        self.capabilities_subscriber_thread = threading.Thread(target=self.__run_capabilities_subscriber_thread, args=())
        self.capabilities_subscriber_thread.daemon = True

        self.capabilities_replier_thread = threading.Thread(target=self.__run_capabilities_replier_thread, args=())
        self.capabilities_replier_thread.daemon = True

        self.deploy_image_replier_thread = threading.Thread(target=self.__run_deploy_image_replier_thread, args=())
        self.deploy_image_replier_thread.daemon = True

        self.image_status_replier_thread = threading.Thread(target=self.__run_image_status_replier_thread, args=())
        self.image_status_replier_thread.daemon = True

        self.image_terminate_thread = threading.Thread(target=self.__run_image_termiate_thread, args=())
        self.image_terminate_thread.daemon = True

        self.stopped = False
        self.after_capabilities_request_handler = None

    @property
    def after_capabilities_request(self):
        return self.after_capabilities_request_handler

    @after_capabilities_request.setter
    def after_capabilities_request(self, handler):
        self.after_capabilities_request_handler = handler

    def start(self):
        """
        Starts the listening on a given port.
        This method will be executed on a separate thread.
        """

        self.capabilities_subscriber.bind('tcp://*:%s' % config['LABELINGENGINE']['port'])
        self.capabilities_subscriber.setsockopt_string(zmq.SUBSCRIBE, 'labelingevent')
        self.capabilities_subscriber_thread.start()

        self.capabilities_replier.bind('tcp://*:%s' % config['CAPABILITIES_REPLIER']['port'])
        self.capabilities_replier_thread.start()

        self.deploy_image_replier.bind('tcp://*:%s' % config['DEPLOY_IMAGE_REPLIER']['port'])
        self.deploy_image_replier_thread.start()

        self.image_status_replier.bind('tcp://*:%s' % config['IMAGE_STATUS_REPLIER']['port'])
        self.image_status_replier_thread.start()

        self.image_terminate_replier.bind('tcp://*:%s' % config['IMAGE_TERMINATE_REPLIER']['port'])
        self.image_terminate_thread.start()

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

    def __run_capabilities_replier_thread(self):
        """
        Private function which is be executed after the start method is called.
        The method will wait for an event where it is subscribed on.
        After receiving an event a list with all the available capabilities will be send to the client who sends the
        request.
        """

        while not self.stopped:
            result = self.capabilities_replier.recv_string()
            if self.after_capabilities_request_handler:
                self.after_capabilities_request_handler(self.capabilities_replier)
            else:
                self.capabilities_replier.send_string(json.dumps([]))

    def __run_deploy_image_replier_thread(self):
        while not self.stopped:
            result = self.deploy_image_replier.recv_string()
            try:
                image = json.loads(result)
                # TODO: check json
                self.valmanager.instantiate(image=image, plugin_type='docker')
            except json.JSONDecodeError:
                pass

    def __run_image_status_replier_thread(self):
        while not self.stopped:
            result = self.image_status_replier.recv_string()
            # TODO: send image status

    def __run_image_termiate_thread(self):
        while not self.stopped:
            image_id = self.image_terminate_replier.recv_string()
            self.valmanager.terminate(instance_name=image_id, plugin_type='docker')

    def request_capabilities(self, ip):
        """
        Method to request all capabilities from another node.
        Will request via the `ZeroMQ.REQ` pattern.
        After the request is send, the method will wait for the response.

        :param ip: the IP address of the node to request the capabilities
        :return: the capabilities as a JSON object
        """

        if not ip:
            return None

        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://%s:%s" % (ip, config['CAPABILITIES_REPLIER']['port']))
        socket.send_string("")
        capabilities = socket.recv_string()
        json_capabilities = []
        try:
            json_capabilities = json.loads(capabilities)
        except json.JSONDecodeError:
            self.logger.error("Got invalid json from capability request")
        return json_capabilities

    def deploy_image(self, image):
        if not image or not image.id or not image.node:
            return None

        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://%s:%s" % (image.node, config['DEPLOY_IMAGE_REPLIER']['port']))
        socket.send_string(json.dumps(image))
        external_image_id = socket.recv_string()
        return external_image_id

    def request_image_status(self, image):
        if not image or not image.id or not image.node:
            return None

        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://%s:%s" % (image.node, config['IMAGE_STATUS_REPLIER']['port']))
        socket.send_string(image.id)
        external_image_status = socket.recv_string()
        return external_image_status

    def terminate_image(self, image):
        if not image or not image.id or not image.node:
            return None

        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://%s:%s" % (image.node, config['IMAGE_TERMINATE_REPLIER']['port']))
        socket.send_string(image.id)
        result = socket.recv_string()
