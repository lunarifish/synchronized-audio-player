from threading import Thread
from critical_watcher import criticalWatcher
from audio import updatePos
from connections import *
from user_functions import *
import console
import server
import variables
import sys
import traceback

console.initLogger()

# not that magic consts
server_port = int(sys.argv[1])
controller_server_port = int(sys.argv[2])
CLIENT_STATUS_UPDATER_INTERVAL = 1

log().info(f"Starting server on port {server_port}, {controller_server_port}")

# global variables initiation
variables._init()
variables.set("server_port", server_port)
variables.set("controller_server_port", controller_server_port)
variables.set("isplaying", 0)
variables.set("url", "None")
variables.set("songpos", "None")
variables.set("songlen", "None")
variables.set("stop", False)
variables.set("active_time", 5)
variables.set("last_controller_client", None)


# ok run it
thread_critical_watcher = Thread(target = criticalWatcher, name = "CriticalWatcherThread")
thread_player_timing = Thread(target = updatePos, name = "PlayerTimingThread")
thread_main_server = Thread(target = server.server, name = "MainServerThread", args = (server_port, ))
thread_controller_server = Thread(target = server.controller, name = "ControllerServerThread", args = (controller_server_port, ))
thread_client_status_updater = Thread(target = updateClientStatus, name = "ClientStatusUpdaterThread", args = (CLIENT_STATUS_UPDATER_INTERVAL, ))

thread_critical_watcher.daemon = True

try:
    thread_critical_watcher.start()
    thread_player_timing.start()
    thread_main_server.start()
    thread_controller_server.start()
    thread_client_status_updater.start()
except:
    for i in traceback.format_exc().split("\n"):
        console.log("error").error(i)


# command binding
# format: [command: target function]
INPUT_BINDINGS = {"stop": stop,
                  "status": logStatus,
                  "list": listClients,
                  "ports": listPorts}
console.userInputMode(INPUT_BINDINGS)