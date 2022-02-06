from threading import Thread
from audio import updatePos
from console import *
from connections import *
import server
import variables
import sys
import traceback



# set server port
server_port = int(sys.argv[1])
controller_server_port = int(sys.argv[2])
CLIENT_STATUS_UPDATER_INTERVAL = 1
print(f"Starting server on port {server_port}, {controller_server_port}")


# global variables initiation
variables._init()
variables.set("isplaying", 0)
variables.set("songurl", "none")
variables.set("songpos", "none")
variables.set("songlen", "none")
variables.set("stop", 0)
variables.set("active_time", 5)
variables.set("last_controller_client", None)


# ok run it
thread_timing = Thread(target = updatePos, name = "TimingThread")
thread_main_server = Thread(target = server.server, name = "MainServerThread", args = (server_port, ))
thread_controller_server = Thread(target = server.controller, name = "ControllerServerThread", args = (controller_server_port, ))
thread_client_status_updater = Thread(target = updateClientStatus, name = "ClientStatusUpdaterThread", args = (CLIENT_STATUS_UPDATER_INTERVAL, ))
try:
    thread_timing.start()
    thread_main_server.start()
    thread_controller_server.start()
    thread_client_status_updater.start()
except:
    traceback.print_exc()


# user functions
def stop():
    global thread_timing
    global thread_main_server
    global thread_controller_server
    global thread_client_status_updater

    log("Server stoping")
    variables.set("stop", 1)

    thread_timing.join()
    thread_main_server.join()
    thread_controller_server.join()
    thread_client_status_updater.join()
    sys.exit()
def logStatus():
    log("Current URL: " + variables.get("songurl"))
    log("Current position: " + str(variables.get("songpos")))
    log("Song length: " + str(variables.get("songlen")))
def listPorts(*ip):
    for i in ip[0]:
        if (client_current := Client.getObjByIP(i)) is None:
            log(f"No such client {i}")
        else:
            log(f"Ports used by client {i}: {client_current.ports}")
# command binding
# format: [command: target function]
INPUT_BINDINGS = {"stop": stop,
                  "status": logStatus,
                  "list": Client.listClients,
                  "ports": listPorts}
userInputMode(INPUT_BINDINGS)