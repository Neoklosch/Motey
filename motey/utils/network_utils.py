import socket


def get_own_ip():
    socket_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_connection.connect(('8.8.8.8', 53))
    socket_ip = socket_connection.getsockname()[:1]
    socket_connection.close()
    return socket_ip[0] if socket_ip else None
