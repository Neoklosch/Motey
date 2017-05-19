from daemonize import Daemonize
from time import sleep

from fog_node_engine.communication.apiserver import APIServer
from fog_node_engine.communication.mqttserver import MQTTServer
from fog_node_engine.configuration.configreader import config
from fog_node_engine.database.labeling_database import LabelingDatabase
from fog_node_engine.hardwareevents.hardwareeventengine import HardwareEventEngine
from fog_node_engine.orchestrator.inter_node_orchestrator import LocalOrchestrator
from fog_node_engine.utils import network_utils
from fog_node_engine.utils.logger import Logger
from fog_node_engine.val.valmanager import VALManager


class Core(object):
    def __init__(self, as_daemon=True):
        self.as_daemon = as_daemon
        self.stopped = False
        self.logger = Logger.Instance()
        self.webserver = APIServer(host=config['WEBSERVER']['ip'], port=config['WEBSERVER']['port'])
        self.mqttserver = MQTTServer(host=config['MQTT']['ip'], port=int(config['MQTT']['port']), username=config['MQTT']['username'], password=config['MQTT']['password'], keepalive=int(config['MQTT']['keepalive']))
        self.labeling_engine = LabelingDatabase.Instance()
        self.valmanager = VALManager.Instance()
        self.local_orchestrator = LocalOrchestrator.Instance()
        self.mqttserver.after_connect = self.handle_after_connect
        self.daemon = None

    def start(self):
        if self.as_daemon:
            self.daemon = Daemonize(app=config['GENERAL']['app_name'], pid=config['GENERAL']['pid'], action=self.run)
            self.daemon.start()
        else:
            self.run()

    def run(self):
        self.logger.info('App started')
        self.webserver.start()
        self.mqttserver.start()

        hardwareEventEngine = HardwareEventEngine.Instance()

        while not self.stopped:
            for i in range(2):
                print('round: %s' % str(i))
                sleep(2)
                self.valmanager.exec_command()

    def handle_after_connect(self):
        print('my own ip is: %s' % network_utils.get_own_ip())
        self.mqttserver.publish_new_node(network_utils.get_own_ip())

    def stop(self):
        self.stopped = True
        self.mqttserver.remove_node(network_utils.get_own_ip())
        self.mqttserver.stop()
        self.valmanager.close()
        if self.daemon:
            self.daemon.exit()
        self.logger.info('App closed')
