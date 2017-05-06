import sys
import os
import errno
from time import sleep
from daemonize import Daemonize
from VALmanager import VALManager
from labeling.labelingengine import LabelingEngine
from hardwareevents.hardwareeventengine import HardwareEventEngine
from localorchestrator import LocalOrchestrator
from logbook import Logger, FileHandler, StreamHandler


def init_logger():
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


def main(logger):
    logger.info('App started')
    labeling_engine = LabelingEngine.Instance()
    valmanager = VALManager(labeling_engine)

    localOrchestrator = LocalOrchestrator(logger)
    localOrchestrator.parse_template(os.path.abspath("data/test.yaml"))

    hardwareEventEngine = HardwareEventEngine(labeling_engine)
    subscription = valmanager.observe_commands().subscribe(lambda x: print("Got: %s" % x))
    another = valmanager.observe_commands().subscribe(lambda x: print("Jo: %s" % x))
    for i in range(5):
        if i >= 3:
            another.dispose()
        print('round: %s' % str(i))
        sleep(2)
        valmanager.exec_command()
    subscription.dispose()
    valmanager.close()
    logger.info('App closed')


if __name__ == '__main__':
    try:
        init_logger()
        logger = Logger('Fog Node Prototype')
    except KeyboardInterrupt:
        print('Leaving the app')

    try:
        main(logger)
    except KeyboardInterrupt:
        logger.info('Leaving the app')

    # daemon = Daemonize(app="fog_node_prototype", pid='/var/run/fog_node_prototype.pid', action=main)
    # daemon.start()
