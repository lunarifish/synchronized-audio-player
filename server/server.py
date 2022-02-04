import socket
from variables import *

def getSongPos():
    print("Server thread started")
    DATA_LENGTH = 1024
    # create socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # local information
    PORT = get("server_port")
    ADDRESS = ('', PORT)
    # binding
    tcp_server_socket.bind(ADDRESS)
    tcp_server_socket.listen(128)
    # receive data
    while get("stop") == 0:
        try:
            # wait for connection
            client_socket, clientAddr = tcp_server_socket.accept()
            peer_ip = client_socket.getpeername()
            peer_ip = peer_ip[0] + ":" + str(peer_ip[1])

            # receive data
            DATA_LENGTH = 1024
            data = client_socket.recv(DATA_LENGTH)
            if data.decode("utf-8") == "songpos":
                print(f"[{peer_ip}]: Peer: songpos")
                client_socket.sendall(str(get("songpos")).encode("utf-8"))
                client_socket.close()
            elif data.decode("utf-8") == "url":
                print(f"[{peer_ip}]: Peer: url")
                client_socket.sendall(get("songurl").encode("utf-8"))
                client_socket.close()
            elif data.decode("utf-8") == "isplaying":
                print(f"[{peer_ip}]: Peer: isplaying")
                client_socket.sendall(str(get("isplaying")).encode("utf-8"))
                client_socket.close()
            else:
                print(f"[{peer_ip}]: Connection refused: invalid token")
                client_socket.close()
                print(f"[{peer_ip}]: Disconnected")
            # send data

        except KeyboardInterrupt:
            pass
    tcp_server_socket.close()


def changeSong():
    print("Controller thread started")
    DATA_LENGTH = 8192
    # create socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # local information
    PORT = get("controller_port")
    ADDRESS = ('', PORT)
    # binding
    tcp_server_socket.bind(ADDRESS)
    tcp_server_socket.listen(128)
    # receive data
    while get("stop") == 0:
        try:
            # wait for connection
            client_socket, clientAddr = tcp_server_socket.accept()
            set("code", 2)
            peer_ip = client_socket.getpeername()
            peer_ip = peer_ip[0] + ":" + str(peer_ip[1])
            print(f"(ADMIN THREAD)[{peer_ip}]: Connection established")
            # receive data
            data = client_socket.recv(DATA_LENGTH).decode("utf-8")
            set("songurl", data)
            set("onChange", 1)
            print(f"(ADMIN THREAD)[{peer_ip}]: URL set: {data}, informing clients")
            while get("code") != 1 and get("code") != 0:
                pass
            if get("code") == 1:
                client_socket.sendall("Error: Invalid URL, closing connection".encode("utf-8"))
            else:
                set("isplaying", 1)
                client_socket.sendall("Success: URL set, closing connection".encode("utf-8"))
            # close socket
            client_socket.close()
            print(f"(ADMIN THREAD)[{peer_ip}]: Disconnected")
        except:
            pass
    tcp_server_socket.close()
