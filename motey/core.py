from time import sleep

from daemonize import Daemonize

from motey.communication.apiserver import APIServer
from motey.communication.mqttserver import MQTTServer
from motey.configuration.configreader import config
from motey.repositories.labeling_repository import LabelingRepository
from motey.labelingengine.labelingengine import LabelingEngine
from motey.orchestrator.inter_node_orchestrator import InterNodeOrchestrator
from motey.utils import network_utils
from motey.utils.logger import Logger
from motey.val.valmanager import VALManager


class Core(object):
    """
    This module provides the core functionality of Motey.
    It can be executed as a daemon service or can be executed in foreground.
    It will start an API webserver and a MQTTServer which can be configured via the config.ini file.
    The core will also start all the necessary components like the LabelingDatabase, the VALManager,
    the InterNodeOrchestrator and the HardwareEventEngine.
    After it is started via self.start() it will be executed until self.stop() is executed.
    """

    def __init__(self, as_daemon=True):
        """
        Constructor of the core.

        :param as_daemon: Executes the core as a daemon. Default is True.
        """

        self.as_daemon = as_daemon
        self.stopped = False
        self.daemon = None

        self.logger = Logger.Instance()
        self.logger.info("App started")
        self.webserver = APIServer(host=config['WEBSERVER']['ip'], port=config['WEBSERVER']['port'])
        self.mqttserver = MQTTServer(host=config['MQTT']['ip'], port=int(config['MQTT']['port']), username=config['MQTT']['username'], password=config['MQTT']['password'], keepalive=int(config['MQTT']['keepalive']))
        self.labeling_engine = LabelingRepository.Instance()
        self.valmanager = VALManager.Instance()
        self.inter_node_orchestrator = InterNodeOrchestrator.Instance()
        self.hardware_event_engine = LabelingEngine.Instance()
        self.mqttserver.after_connect = self.after_connect_callback
        self.mqttserver.nodes_request_callback = self.__nodes_request_callback

    def start(self):
        """
        Start the core component. If self.as_daemon is set to True, the component will be started as a daemon services.
        It will use the path to the pid which is configured in the config.ini.
        If self.as_daemon is set to False, the component will be executed in foreground.
        """

        if self.as_daemon:
            self.daemon = Daemonize(app=config['GENERAL']['app_name'], pid=config['GENERAL']['pid'], action=self.run)
            self.daemon.start()
        else:
            self.run()

    def run(self):
        """
        The method is the main app loop.
        It starts the API server as well as the MQTT server and will be executed until self.stop() is executed.
        """

        self.logger.info('Core started')
        self.webserver.start()
        self.mqttserver.start()
        self.hardware_event_engine.start()

        while not self.stopped:
            sleep(.1)

    def restart(self):
        """
        Restart the core.
        """

        self.stop()
        self.start()

    def after_connect_callback(self):
        """
        Will be called after the MQTTServer has established a connection to the broker.
        Send out a request to fetch the ip from all existing nodes.
        """
        self.mqttserver.publish_node_request(network_utils.get_own_ip())

    def __nodes_request_callback(self, client, userdata, message):
        """
        Will be called if a request to fetch the ip from all existing nodes comes in.
        Send out the ip of the node.

        :param client:     the client instance for this callback
        :param userdata:   the private user data as set in Client() or userdata_set()
        :param message:    the data which was send
        """
        self.mqttserver.publish_new_node(network_utils.get_own_ip())

    def stop(self):
        """
        Clean up the started services.
        At first it sends a MQTTServer.remove_node() command.
        Afterwards it will stop the MQTTServer instance as well as the VALManager.
        Finally it stops the daemon if self.as_daemon is set to True.
        """

        self.stopped = True
        self.mqttserver.remove_node(network_utils.get_own_ip())
        self.mqttserver.stop()
        self.valmanager.close()
        self.webserver.stop()
        if self.daemon:
            self.daemon.exit()
        self.logger.info('Core stopped')
