import json
import threading

import zmq
from rx.subjects import Subject

from motey.configuration.configreader import config
from motey.models.image import Image
from motey.models.image_state import ImageState


class ZeroMQServer(object):
    """
    ZeroMQ server to communicate with adjacent fog nodes and to reply to requests.
    The different listeners will be executed in a separate thread and will not block the main thread.
    """

    add_capability_event_stream = Subject()
    remove_capability_event_stream = Subject()

    def __init__(self, logger, valmanager):
        """
        Constructor ot the ZeroMQ server.

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

    def start(self):
        """
        Starts the listening on a given port.
        This method will be executed on a separate thread.
        """

        self.capabilities_subscriber.bind('ipc://%s' % config['ZEROMQ']['capability_engine_ipc_path'])
        self.capabilities_subscriber.setsockopt_string(zmq.SUBSCRIBE, 'add_capability')
        self.capabilities_subscriber.setsockopt_string(zmq.SUBSCRIBE, 'remove_capability')
        self.capabilities_subscriber_thread.start()

        self.capabilities_replier.bind('tcp://*:%s' % config['ZEROMQ']['capabilities_replier'])
        self.capabilities_replier_thread.start()

        self.deploy_image_replier.bind('tcp://*:%s' % config['ZEROMQ']['deploy_image_replier'])
        self.deploy_image_replier_thread.start()

        self.image_status_replier.bind('tcp://*:%s' % config['ZEROMQ']['image_status_replier'])
        self.image_status_replier_thread.start()

        self.image_terminate_replier.bind('tcp://*:%s' % config['ZEROMQ']['image_terminate_replier'])
        self.image_terminate_thread.start()

        self.logger.info('ZeroMQ server started')

    def stop(self):
        """
        Should be executed to clean up the capability engine
        """

        self.logger.info('ZeroMQ server stopped')

    def __run_capabilities_subscriber_thread(self):
        """
        Private function which is be executed after the start method is called.
        The method will wait for an event where it is subscribed on.
        After receiving an event a new capability will be added to the capability database.
        """

        while not self.stopped:
            result = self.capabilities_subscriber.recv_string()
            topic, output = result.split('#', 1)
            if topic == 'add_capability':
                self.add_capability_event_stream.on_next(output)
            elif topic == 'remove_capability':
                self.remove_capability_event_stream.on_next(output)

    def __run_capabilities_replier_thread(self):
        """
        Private function which is be executed after the start method is called.
        The method will wait for an event where it is subscribed on.
        After receiving an event a list with all the available capabilities will be send to the client who sends the
        request.
        """

        while not self.stopped:
            result = self.capabilities_replier.recv_string()
            self.capabilities_replier.send_string(json.dumps([]))

    def __run_deploy_image_replier_thread(self):
        """
        Private function which is be executed after the start method is called.
        The method will wait for an event where it is subscribed on.
        After receiving an event the data will be parsed as JSON and validated.
        Afterwards it will be used to instantiate an image instance.
        Finally it will send out the id of the instantiated instance or None if something went wrong.
        """
        while not self.stopped:
            result = self.deploy_image_replier.recv_string()
            image_id = None
            try:
                image_json = json.loads(result)
                image = Image.transform(image_json)
                if image:
                    image_id = self.valmanager.instantiate(image=image)
            except json.JSONDecodeError:
                pass
            self.deploy_image_replier.send_string(image_id if image_id else '')

    def __run_image_status_replier_thread(self):
        """
        Private function which is be executed after the start method is called.
        The method will wait for an event where it is subscribed on.
        After receiving an event the ``ImageState`` of an image instance will be returned.
        """
        while not self.stopped:
            result = self.image_status_replier.recv_string()
            state = ImageState.ERROR
            try:
                image_json = json.loads(result)
                image = Image.transform(image_json)
                if image:
                    state = self.valmanager.get_instance_state(image=image)
            except json.JSONDecodeError:
                state = ImageState.ERROR
            self.image_status_replier.send_string(state)

    def __run_image_termiate_thread(self):
        """
        Private function which is be executed after the start method is called.
        The method will wait for an event where it is subscribed on.
        After receiving an event the image instance which matches the send id will be terminated.
        """
        while not self.stopped:
            result = self.image_terminate_replier.recv_string()
            try:
                image_json = json.loads(result)
                image = Image.transform(image_json)
                if image:
                    self.valmanager.terminate(image=image)
            except json.JSONDecodeError:
                pass
            self.image_terminate_replier.send_string('')

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
        socket.connect("tcp://%s:%s" % (ip, config['ZEROMQ']['capabilities_replier']))
        socket.send_string("")
        capabilities = socket.recv_string()
        json_capabilities = []
        try:
            json_capabilities = json.loads(capabilities)
        except json.JSONDecodeError:
            self.logger.error("Got invalid json from capability request")
        return json_capabilities

    def deploy_image(self, image):
        """
        Will deploy an image to the node stored in the ``Image.node`` attribute.

        :param image: Image to be deployed.
        :type image: motey.models.image.Image
        :return: the id of the deployed image or None if something went wrong.
        """

        if not image or not image.node:
            return None

        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://%s:%s" % (image.node, config['ZEROMQ']['deploy_image_replier']))
        socket.send_string(json.dumps(dict(image)))
        external_image_id = socket.recv_string()
        return external_image_id

    def request_image_status(self, image):
        """
        Request the status of an specific ``ImageState`` instance or ``ImageState.ERROR`` if something went
        wrong.

        :param image: Image to be used to get the status.
        :type image: motey.models.image.Image
        :return: the ``ImageState`` or ``ImageState.ERROR`` if something went wrong
        """
        if not image or not image.id or not image.node:
            return None

        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://%s:%s" % (image.node, config['ZEROMQ']['image_status_replier']))
        socket.send_string(json.dumps(dict(image)))
        external_image_status = socket.recv_string()
        return external_image_status

    def terminate_image(self, image):
        """
        Will terminate an image instance.

        :param image: the image instance to be terminated
        :type image: motey.models.image.Image
        """
        if not image or not image.id or not image.node:
            return None

        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://%s:%s" % (image.node, config['ZEROMQ']['image_terminate_replier']))
        socket.send_string(json.dumps(dict(image)))
        result = socket.recv_string()
