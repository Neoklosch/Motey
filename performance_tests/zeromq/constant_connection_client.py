import zmq
import datetime

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

example_string = '{"name": "alpine", "engine": "docker", "parameters": {"ports": ["80/tcp: 8080", "7070/udp: 9001"],' \
                 '"name": "alpine_from_motey"}, "capabilities": ["alpine", "docker", "zigbee"]}'
start_time = datetime.datetime.now()

for request in range(10000):
    socket.send_string(example_string)
    message = socket.recv()

end_time = datetime.datetime.now()
delta = end_time - start_time
print(delta)
