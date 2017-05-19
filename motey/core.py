from daemonize import Daemonize

from motey.communication.apiserver import APIServer
from motey.communication.mqttserver import MQTTServer
from motey.configuration.configreader import config
from motey.database.labeling_database import LabelingDatabase
from motey.hardwareevents.hardwareeventengine import HardwareEventEngine
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
        self.as_daemon = as_daemon
        self.stopped = False
        self.logger = Logger.Instance()
        self.webserver = APIServer(host=config['WEBSERVER']['ip'], port=config['WEBSERVER']['port'])
        self.mqttserver = MQTTServer(host=config['MQTT']['ip'], port=int(config['MQTT']['port']), username=config['MQTT']['username'], password=config['MQTT']['password'], keepalive=int(config['MQTT']['keepalive']))
        self.labeling_engine = LabelingDatabase.Instance()
        self.valmanager = VALManager.Instance()
        self.inter_node_orchestrator = InterNodeOrchestrator.Instance()
        self.mqttserver.after_connect = self.__handle_after_connect
        self.daemon = None

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
        self.logger.info('App started')
        self.webserver.start()
        self.mqttserver.start()

        hardwareEventEngine = HardwareEventEngine.Instance()

        while not self.stopped:
            pass

    def restart(self):
        """
        Restart the core.

        """
        self.stop()
        self.start()

    def __handle_after_connect(self):
        """
        Will be called after the MQTTServer has established a connection to the broker.

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
        if self.daemon:
            self.daemon.exit()
        self.logger.info('App closed')
