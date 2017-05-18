import docker
import signal
import sys


def signal_handler(signal, frame):
    print('shutdown...')
    sys.exit(0)


def main():
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    kwargs = {
        'ports': {
            '5238/tcp': 5239
        },
        'name': 'fog_node_alpine'
    }
    client.containers.run(image='alpine', **kwargs)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
