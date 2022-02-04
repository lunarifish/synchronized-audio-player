import socket

def sendData(host, port, message):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = (host, port)
    tcp_socket.connect(server)

    tcp_socket.send(message.encode("utf-8"))

    data_length = 1024
    data = tcp_socket.recv(data_length).decode("utf-8")

    tcp_socket.close()
    return data