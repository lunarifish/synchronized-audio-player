import socket
import traceback
from variables import *
from connections import *
from console import log

STOP_MESSAGE = "stop"

def server(port):
    log().info("Server thread started")
    DATA_LENGTH = 1024
    VALID_MESSAGES = ["songpos", "url", "isplaying"]
    try:
        # create socket
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # local information
        ADDRESS = ('', port)
        # binding
        tcp_server_socket.bind(ADDRESS)
        tcp_server_socket.listen(128)
    except:
        for i in traceback.format_exc().split("\n"):
            log("critical").critical(i)
        set("critical", True)
        set("stop", True)
    # receive data
    while not get("stop"):
        try:
            # wait for connection
            client_socket, clientAddr = tcp_server_socket.accept()
            peer = client_socket.getpeername()
            current_client = Client.getObjByIP(ip = peer[0])
            if current_client is None:
                current_client = Client(ip = peer[0], port = peer[1])
                Client.clients.append(current_client)
            # process request
            DATA_LENGTH = 1024
            data = client_socket.recv(DATA_LENGTH).decode("utf-8")
            if data in VALID_MESSAGES:
                current_client.newRequest(request = data, port = peer[1])
                client_socket.sendall(str(get(data)).encode("utf-8"))
                client_socket.close()
            elif data == "stop" and current_client.ip == "127.0.0.1":
                break
            else:
                log("warn").warning(f"[{peer_ip}]: Connection refused: invalid token")
                client_socket.close()
        except:
            for i in traceback.format_exc().split("\n"):
                log("error").error(i)
    log().info(f"Release port {port}")
    tcp_server_socket.close()
    log().info("Thread stopping")


def controller(port):
    log().info("Controller thread started")
    DATA_LENGTH = 8192
    url_backup = get("url")
    try:
        # create socket
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # local information
        ADDRESS = ('', port)
        # binding
        tcp_server_socket.bind(ADDRESS)
        tcp_server_socket.listen(128)
    except:
        for i in traceback.format_exc().split("\n"):
            log("critical").critical(i)
        set("stop", True)
        set("critical", True)
    # receive data
    while not get("stop"):
        try:
            # wait for connection
            client_socket, clientAddr = tcp_server_socket.accept()
            set("code", 2) # code = 2 -> received request, processing
            peer = client_socket.getpeername()
            controller = Controller(ip = peer[0], port = peer[1])
            # receive data
            data = client_socket.recv(DATA_LENGTH).decode("utf-8")
            if data == "stop" and controller.ip == "127.0.0.1":
                break
            url_backup = get("url")
            set("url", data)
            set("onChange", 1)
            controller.newCommand(command = data, port = peer[1])
            while get("code") != 1 and get("code") != 0:
                pass
            if get("code") == 1:
                set("url", url_backup)
                set("onChange", 0)
                log("error").error(f"Got invalid URL from controller command: {data}, keep current")
                log().info(f"To controller[{controller.ip}]: Error: Invalid URL, closing connection")
                client_socket.sendall("Error: Invalid URL, closing connection".encode("utf-8"))
            else:
                set("isplaying", 1)
                log().info(f"To controller[{controller.ip}]: Success: URL set: {data}, closing connection")
                client_socket.sendall(f"Success: URL set: {data}, closing connection".encode("utf-8"))
            # close socket
            client_socket.close()
        except:
            for i in traceback.format_exc().split("\n"):
                log("error").error(i)
    log().info(f"Release port {port}")
    tcp_server_socket.close()
    log().info("Thread stopping")

def stopServer(port, host = "localhost"):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (host, port)
    tcp_socket.connect(server_addr)
    tcp_socket.send(STOP_MESSAGE.encode("utf-8"))
    tcp_socket.close()
