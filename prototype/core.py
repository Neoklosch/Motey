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

    def stop(self):
        self.stopped = True

    def start(self):
        self.logger.info('App started')
        self.webserver.start()
        labeling_engine = LabelingEngine.Instance()
        valmanager = VALManager(labeling_engine)

        localOrchestrator = LocalOrchestrator(self.logger)
        localOrchestrator.parse_template(os.path.abspath("data/test.yaml"))

        hardwareEventEngine = HardwareEventEngine(labeling_engine)
        subscription = valmanager.observe_commands().subscribe(lambda x: print("Got: %s" % x))
        another = valmanager.observe_commands().subscribe(lambda x: print("Jo: %s" % x))

        while not self.stopped:
            for i in range(2):
                if i >= 3:
                    another.dispose()
                print('round: %s' % str(i))
                sleep(2)
                valmanager.exec_command()

        subscription.dispose()
        valmanager.close()
        self.logger.info('App closed')

