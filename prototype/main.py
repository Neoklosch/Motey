from time import sleep
from daemonize import Daemonize
from DockerVAL import DockerVAL


def main():
    f = open('/tmp/workfile.txt', 'w')
    dockerval = DockerVAL()
    for i in range(5):
        print('round: %s' % str(i))
        sleep(5)
        f.write('This is a test\n')
        dockerval.hasImage('keks')

    f.write('the end')
    f.close()

if __name__ == '__main__':
    main()
    # daemon = Daemonize(app="fog_node_prototype", pid='/var/run/fog_node_prototype.pid', action=main)
    # daemon.start()
