import sys
import os
import errno
import signal
from logbook import Logger, FileHandler, StreamHandler
from prototype.core import Core
from prototype.api.apiserver import APIServer
from prototype.config import config


core = apiserver = None


def signal_handler(signal, frame):
    if core:
        core.stop()
    sys.exit(0)


def init_logger():
    logger = Logger(config['LOGGER']['name'])
    logger_path = config['LOGGER']['log_path']
    try:
        os.makedirs(logger_path)
    except OSError as oserror:
        if oserror.errno == errno.EEXIST and os.path.isdir(logger_path):
            pass
        else:
            raise

    StreamHandler(sys.stdout).push_application()
    log_handler = FileHandler('%s%s' % (logger_path, config['LOGGER']['file_name']))
    log_handler.push_application()
    return logger


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    logger = init_logger()
    apiserver = APIServer(logger)
    core = Core(apiserver, logger)
    core.start()
