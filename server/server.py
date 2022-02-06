import socket
import traceback
from variables import *
from connections import *
from console import log


def server(PORT):
    log().info("Server thread started")
    DATA_LENGTH = 1024
    VALID_MESSAGES = ["songpos", "url", "isplaying"]
    try:
        # create socket
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # local information
        ADDRESS = ('', PORT)
        # binding
        tcp_server_socket.bind(ADDRESS)
        tcp_server_socket.listen(128)
    except:
        for i in traceback.format_exc().split("\n"):
            log("critical").critical(i)
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
            # process request
            DATA_LENGTH = 1024
            data = client_socket.recv(DATA_LENGTH)
            if (data := data.decode("utf-8")) in VALID_MESSAGES:
                current_client.newRequest(request = data, port = peer[1])
                client_socket.sendall(str(get(data)).encode("utf-8"))
                client_socket.close()
            else:
                log("warn").warning(f"[{peer_ip}]: Connection refused: invalid token")
                client_socket.close()
        except:
            for i in traceback.format_exc().split("\n"):
                log("error").error(i)
    tcp_server_socket.close()


def controller(PORT):
    log().info("Controller thread started")
    DATA_LENGTH = 8192
    url_backup = get("url")
    try:
        # create socket
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # local information
        ADDRESS = ('', PORT)
        # binding
        tcp_server_socket.bind(ADDRESS)
        tcp_server_socket.listen(128)
    except:
        for i in traceback.format_exc().split("\n"):
            log("critical").critical(i)
    # receive data
    while get("stop") == 0:
        try:
            # wait for connection
            client_socket, clientAddr = tcp_server_socket.accept()
            set("code", 2) # code = 2 -> received request, processing
            peer = client_socket.getpeername()
            controller = Controller(ip = peer[0], port = peer[1])
            # receive data
            data = client_socket.recv(DATA_LENGTH).decode("utf-8")
            url_backup = get("url")
            set("url", data)
            set("onChange", 1)
            controller.newCommand(command = data, port = peer[1])
            while get("code") != 1 and get("code") != 0:
                pass
            if get("code") == 1:
                set("url", url_backup)
                set("onChange", 0)
                log("error").error("Got invalid URL from controller command")
                client_socket.sendall("Error: Invalid URL, closing connection".encode("utf-8"))
            else:
                log().info("Download finished")
                set("isplaying", 1)
                log().info(f"Controller[{controller.ip}]: URL set: {data}")
                client_socket.sendall("Success: URL set, closing connection".encode("utf-8"))
            # close socket
            client_socket.close()
        except:
            for i in traceback.format_exc().split("\n"):
                log("error").error(i)
    tcp_server_socket.close()
