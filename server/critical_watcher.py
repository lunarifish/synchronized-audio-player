import threading
from variables import *
from user_functions import stop
from console import log


def criticalWatcher():
    log().info("Critical watcher thread started")
    while len(threading.enumerate()) != 2:
        if get("critical"):
            log("critical").critical("Critical error detected, stopping server")
            stop(critical = True)
    log().info("Thread stopping")