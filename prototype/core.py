import threading
import sys
import os
import errno
from time import sleep
from VALmanager import VALManager
from labeling.labelingengine import LabelingEngine
from hardwareevents.hardwareeventengine import HardwareEventEngine
from localorchestrator import LocalOrchestrator
from logbook import Logger, FileHandler, StreamHandler

class Core(object):
    def __init__(self, webserver):
        self.stopped = False
        self.init_logger()
        self.logger = Logger('Fog Node Prototype')
        self.app = webserver
        self.looper = None

    def stop(self):
        self.stopped = True
        self.app.stop()

    def start(self):
        self.logger.info('App started')
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

    def init_logger(self):
        logger_path = '/var/log/fog_node_prototype/'
        try:
            os.makedirs(logger_path)
        except OSError as oserror:
            if oserror.errno == errno.EEXIST and os.path.isdir(logger_path):
                pass
            else:
                raise

        StreamHandler(sys.stdout).push_application()
        log_handler = FileHandler('%sapplication.log' % logger_path)
        log_handler.push_application()

    def run_server(self):
        self.app.use_reloader = False
        self.app.run(host="0.0.0.0", port=5023)

    def start_api(self):
        self.api_thread = threading.Thread(target = self.run_server)
        self.api_thread.start()
