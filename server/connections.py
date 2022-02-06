import time
import variables
from console import log

class Controller:
    def __init__(self, ip = None, port = None, command = None):
        self.ip = ip
        self.port = port
        self.command = command
        self.control_time = time.time()

class Client:
    clients = []
    clients_count = 0
    active_clients = []
    inactive_clients = []
    def __init__(self, ip, port, request = None):
        self.id = Client.clients_count
        self.ip = ip
        self.request = request
        self.ports = [port]
        self.last_com_time = time.time()
        self.is_active = True
        Client.clients_count += 1
    def newRequest(self, request, port):
        if port not in self.ports:
            self.ports.append(port)
        self.request = request
        self.last_com_time = time.time()
    def isActive(self):
        if time.time() - self.last_com_time > variables.get("active_time"):
            return False
        else:
            return True

    def getObjByIP(ip):
        for i in Client.clients:
            if i.ip == ip:
                return i
        return None
    def listClients():
        controller = variables.get("last_controller_client")
        Client.refreshActiveTimer()
        if controller is not None:
            log(f"Last controller: {controller.ip}:{controller.port} at {time.asctime(time.localtime(controller.control_time))}")
            log(f"URL: {controller.command}\n")
        log(f"Active: {', '.join([i.ip for i in Client.active_clients])}")
        log(f"Inactive: {', '.join([i.ip for i in Client.inactive_clients])}")
    def refreshActiveTimer():
        Client.active_clients.clear()
        Client.inactive_clients.clear()
        for i in Client.clients:
            i.is_active = i.isActive()
            if i.is_active:
                Client.active_clients.append(i)
            else:
                Client.inactive_clients.append(i)

def updateClientStatus(interval):
    print("Client status updater thread started")
    log(f"time interval: {interval}s")
    while variables.get("stop") == 0:
        before_refresh = [i for i in Client.inactive_clients]
        Client.refreshActiveTimer()
        for i in Client.inactive_clients:
            if i not in before_refresh:
                log(f"Client {i.ip} is now inactive")
        time.sleep(interval)
    log("Thread stop")