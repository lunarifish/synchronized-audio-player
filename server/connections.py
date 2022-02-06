import time
import variables
from console import log

class Controller:
    last_controller = None
    def __init__(self, ip, port, command = None):
        self.ip = ip
        self.port = port
        self.command = command
        self.control_time = time.time()
        Controller.last_controller = self
        log().info(f"New controller connection: {self.ip}:{self.port}")
    def newCommand(self, command, port):
        Controller.last_controller = self
        self.port = port
        self.command = command
        self.control_time = time.time()
        log().info(f"Controller[{self.ip}:{self.port}]: {command}")


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
        log().info(f"New client: {self.ip}")
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
    def refreshActiveTimer():
        Client.active_clients.clear()
        Client.inactive_clients.clear()
        for i in Client.clients:
            i.is_active = i.isActive()
            if i.is_active:
                Client.active_clients.append(i)
            else:
                Client.inactive_clients.append(i)

def listClients():
    last_controller = Controller.last_controller
    if last_controller is not None:
        log().info(f"Last controller activity: {last_controller.ip}:{last_controller.port} at {time.asctime(time.localtime(last_controller.control_time))}")
        log().info(f"Message: {last_controller.command}\n")
    else:
        log().info("Last controller activity: None")
    log().info(f"Active clients: {', '.join([i.ip for i in Client.active_clients])}")
    log().info(f"Inactive clients: {', '.join([i.ip for i in Client.inactive_clients])}")

def updateClientStatus(interval):
    log().info("Client status updater thread started")
    log().info(f"time interval: {interval}s")
    while variables.get("stop") == 0:
        before_refresh = [i for i in Client.inactive_clients]
        Client.refreshActiveTimer()
        for i in Client.inactive_clients:
            if i not in before_refresh:
                log().info(f"Client {i.ip} is now inactive")
        time.sleep(interval)
    log().info("Thread stopping")