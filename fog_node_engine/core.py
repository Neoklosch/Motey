from time import sleep

from fog_node_engine.communication.apiserver import APIServer
from fog_node_engine.communication.mqttserver import MQTTServer
from fog_node_engine.hardwareevents.hardwareeventengine import HardwareEventEngine
from fog_node_engine.labeling.labelingengine import LabelingEngine
from fog_node_engine.orchestrator.inter_node_orchestrator import LocalOrchestrator
from fog_node_engine.utils.logger import Logger
from fog_node_engine.val.valmanager import VALManager


class Core(object):
    def __init__(self):
        self.stopped = False
        self.logger = Logger.Instance()
        self.webserver = APIServer.Instance()
        self.mqttserver = MQTTServer.Instance()
        self.labeling_engine = LabelingEngine.Instance()
        self.valmanager = VALManager.Instance()
        self.local_orchestrator = LocalOrchestrator.Instance()

    def start(self):
        self.logger.info('App started')
        self.webserver.start()
        self.mqttserver.start()

        hardwareEventEngine = HardwareEventEngine.Instance()
        self.subscription = self.valmanager.observe_commands().subscribe(lambda x: print("Got: %s" % x))
        another = self.valmanager.observe_commands().subscribe(lambda x: print("Jo: %s" % x))

        while not self.stopped:
            for i in range(2):
                if i >= 3:
                    another.dispose()
                print('round: %s' % str(i))
                sleep(2)
                self.valmanager.exec_command()

    def stop(self):
        self.stopped = True
        self.mqttserver.stop()
        self.subscription.dispose()
        self.valmanager.close()
        self.logger.info('App closed')
