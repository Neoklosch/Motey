from time import sleep
from daemonize import Daemonize
from DockerVAL import DockerVAL
from VALManager import VALManager


def main():
    dockerval = DockerVAL()
    valmanager = VALManager()
    subscription = valmanager.observeCommands().subscribe(lambda x: print("Got: %s" % x))
    another = valmanager.observeCommands().subscribe(lambda x: print("Jo: %s" % x))
    for i in range(5):
        if i >= 3:
            another.dispose()
        print('round: %s' % str(i))
        sleep(2)
        print(dockerval.hasImage('46102226f2'))
        valmanager.execCommand()
    subscription.dispose()


if __name__ == '__main__':
    main()
    # daemon = Daemonize(app="fog_node_prototype", pid='/var/run/fog_node_prototype.pid', action=main)
    # daemon.start()
