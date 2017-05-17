import zmq
from time import sleep


def main():
    context = zmq.Context()

    print('Connecting to server...')
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:5234')

    #  Do 10 requests, waiting each time for a response
    for index in range(10):
        print('Sending request with message: 192.168.0.%s' % index)
        socket.send_string('192.168.0.%s' % index)

        #  Get the reply.
        message = socket.recv()
        print('Received %s' % message)
        sleep(3)


if __name__ == '__main__':
    main()
