from time import sleep

from prototype.communication.apiserver import APIServer
from prototype.communication.mqttserver import MQTTServer
from prototype.hardwareevents.hardwareeventengine import HardwareEventEngine
from prototype.labeling.labelingengine import LabelingEngine
from prototype.orchestrator.inter_node_orchestrator import LocalOrchestrator
from prototype.utils.logger import Logger
from prototype.val.valmanager import VALManager


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
