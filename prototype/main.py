import sys
import os
import errno
from core import Core
from api.apiserver import APIServer
from logbook import Logger, FileHandler, StreamHandler
from config import config


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
    logger = init_logger()
    apiserver = APIServer(logger)
    core = Core(apiserver, logger)
    try:
        core.start()
    except KeyboardInterrupt as exc:
        core.stop()


