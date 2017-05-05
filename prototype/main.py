from time import sleep
from daemonize import Daemonize
from VALmanager import VALManager
from labeling.labelingengine import LabelingEngine


def main():
    labeling_engine = LabelingEngine.Instance()
    valmanager = VALManager(labeling_engine)
    subscription = valmanager.observeCommands().subscribe(lambda x: print("Got: %s" % x))
    another = valmanager.observeCommands().subscribe(lambda x: print("Jo: %s" % x))
    for i in range(5):
        if i >= 3:
            another.dispose()
        print('round: %s' % str(i))
        sleep(2)
        valmanager.execCommand()
    subscription.dispose()


if __name__ == '__main__':
    main()
    # daemon = Daemonize(app="fog_node_prototype", pid='/var/run/fog_node_prototype.pid', action=main)
    # daemon.start()
