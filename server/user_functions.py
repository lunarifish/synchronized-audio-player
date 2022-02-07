import threading
import time
import sys
import os
from file import cleanTempFile
from server import stopServer
from console import log
from variables import *
from connections import Controller, Client



'''these functions will work in console user input mode
    so i call them user functions
    believe me i am naming them right'''

# btw don't forget to bind a command in main.py



def stop(critical = False):
    log().info("Server stopping")
    cleanTempFile()
    log().info("Cleaned temp files")
    set("stop", True)
    stopServer(get("server_port"))
    stopServer(get("controller_server_port"))
    if critical:
        for thread in threading.enumerate():
            if thread.getName() != "MainThread" and thread.getName() != "CriticalWatcherThread":
                thread.join()
        os._exit(1)
    else:
        for thread in threading.enumerate():
            if thread.getName() != "MainThread":
                thread.join()
        os._exit(0)

def logStatus():
    log().info("Current URL: " + get("url"))
    log().info("Current position: " + str(get("songpos")))
    log().info("Song length: " + str(get("songlen")))

def listClients():
    last_controller = Controller.last_controller
    if last_controller is not None:
        log().info(f"Last controller activity: {last_controller.ip}:{last_controller.port} at {time.asctime(time.localtime(last_controller.control_time))}")
        log().info(f"Message: {last_controller.command}\n")
    else:
        log().info("Last controller activity: None")
    log().info(f"Active clients: {', '.join([i.ip for i in Client.active_clients])}")
    log().info(f"Inactive clients: {', '.join([i.ip for i in Client.inactive_clients])}")

def listPorts(*ip):
    for i in ip[0]:
        if (client_current := Client.getObjByIP(i)) is None:
            log().info(f"No such client {i}")
        else:
            log().info(f"Ports used by client {i}: {client_current.ports}")
