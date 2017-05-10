import os
from time import sleep
from VALmanager import VALManager
from labeling.labelingengine import LabelingEngine
from hardwareevents.hardwareeventengine import HardwareEventEngine
from localorchestrator import LocalOrchestrator


class Core(object):
    def __init__(self, webserver, logger):
        self.stopped = False
        self.logger = logger
        self.webserver = webserver
        self.labeling_engine = LabelingEngine.Instance()
        self.local_orchestrator = LocalOrchestrator(self.logger)
        self.valmanager = VALManager(self.logger, self.labeling_engine, self.local_orchestrator)

    def start(self):
        self.logger.info('App started')
        self.webserver.start()

        hardwareEventEngine = HardwareEventEngine(self.labeling_engine)
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
        self.subscription.dispose()
        self.valmanager.close()
        self.logger.info('App closed')



