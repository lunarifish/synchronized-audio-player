import socket
import traceback
from variables import *
from connections import *
from console import log


def server(PORT):
    print("Server thread started")
    DATA_LENGTH = 1024
    # create socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # local information
    ADDRESS = ('', PORT)
    # binding
    tcp_server_socket.bind(ADDRESS)
    tcp_server_socket.listen(128)
    # receive data
    while get("stop") == 0:
        try:
            # wait for connection
            client_socket, clientAddr = tcp_server_socket.accept()
            peer = client_socket.getpeername()
            current_client = Client.getObjByIP(ip = peer[0])
            if current_client is None:
                current_client = Client(ip = peer[0], port = peer[1])
                Client.clients.append(current_client)
                log(f"New client: {current_client.ip}")
            # process request
            DATA_LENGTH = 1024
            data = client_socket.recv(DATA_LENGTH)
            if data.decode("utf-8") == "songpos":
                current_client.newRequest(request = "songpos", port = peer[1])
                client_socket.sendall(str(get("songpos")).encode("utf-8"))
                client_socket.close()
            elif data.decode("utf-8") == "url":
                current_client.newRequest(request = "url", port = peer[1])
                client_socket.sendall(get("songurl").encode("utf-8"))
                client_socket.close()
            elif data.decode("utf-8") == "isplaying":
                current_client.newRequest(request = "isplaying", port = peer[1])
                client_socket.sendall(str(get("isplaying")).encode("utf-8"))
                client_socket.close()
            else:
                log(f"[{peer_ip}]: Connection refused: invalid token")
                client_socket.close()
                log(f"[{peer_ip}]: Disconnected")
        except:
            traceback.print_exc()
    tcp_server_socket.close()


def controller(PORT):
    print("Controller thread started")
    DATA_LENGTH = 8192
    # create socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # local information
    ADDRESS = ('', PORT)
    # binding
    tcp_server_socket.bind(ADDRESS)
    tcp_server_socket.listen(128)
    # receive data
    while get("stop") == 0:
        try:
            # wait for connection
            client_socket, clientAddr = tcp_server_socket.accept()
            set("code", 2) # code = 2 -> received request, processing
            controller = Controller()
            peer = client_socket.getpeername()
            controller.ip = peer[0]
            controller.port = peer[1]
            log(f"New controller connection: {controller.ip}:{controller.port}")
            # receive data
            data = client_socket.recv(DATA_LENGTH).decode("utf-8")
            controller.command = data
            set("last_controller_client", controller)
            set("songurl", data)
            set("onChange", 1)
            log(f"[{peer_ip}]: URL set: {data}")
            while get("code") != 1 and get("code") != 0:
                pass
            if get("code") == 1:
                client_socket.sendall("Error: Invalid URL, closing connection".encode("utf-8"))
            else:
                set("isplaying", 1)
                client_socket.sendall("Success: URL set, closing connection".encode("utf-8"))
            # close socket
            client_socket.close()
            log(f"[{peer_ip}]: Disconnected")
        except:
            traceback.print_exc()
    tcp_server_socket.close()
