import socket
def sendData(host, port, data):
    # create socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server
    server_addr = (host, port)
    tcp_socket.connect(server_addr)
    # send data
    tcp_socket.send(data.encode("utf-8"))
    data_length = 1024
    data = tcp_socket.recv(data_length).decode("utf-8")
    print(f"Server: {data}")
    # close socket
    tcp_socket.close()