import signal
import sys

from motey.di.app_module import Application

core = None


def signal_handler(signal, frame):
    if core:
        core.stop()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    core = Application.core(as_daemon=False)
    core.start()
