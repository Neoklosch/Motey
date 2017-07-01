import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

example_container_id = "346cddf529f3a92d49d6d2b6a8ceb2154eff14709c10123ef1432029e4f2864a"
while True:
    message = socket.recv_string()
    socket.send_string(example_container_id)
