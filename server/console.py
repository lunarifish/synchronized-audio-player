import threading
import logging
import time
import os

LOGGER_LEVELS_NORMAL = ["debug", "info"]
LOGGER_LEVELS_WARN = ["warn", "error", "critical"]

def initLogger():
    global logger
    global error_logger
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    error_logger = logging.getLogger("error_logger")

    formatter_info = logging.Formatter("[%(asctime)s][%(threadName)s %(levelname)s]: %(message)s")
    formatter_debug = logging.Formatter("[%(asctime)s][%(filename)s-%(funcName)s()][%(threadName)s %(levelname)s]: %(message)s")
    debug_log_name = time.strftime("%Y%m%d%H%M%S") + ".log"
    try: debug_log_path = os.path.dirname(os.getcwd()) + "/" + debug_log_name
    except: print(r"Logger: can't get current dictionary")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter_info)
    console_warn_handler = logging.StreamHandler()
    console_warn_handler.setLevel(logging.WARN)
    console_warn_handler.setFormatter(formatter_debug)
    debug_handler = logging.FileHandler(debug_log_path, mode = "w")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter_debug)

    logger.addHandler(console_handler)
    logger.addHandler(debug_handler)
    error_logger.addHandler(console_warn_handler)
    error_logger.addHandler(debug_handler)
    logger.info("Logger initiated")
    logger.info(f"logfile: {debug_log_path}")

def log(type = "info"):
    if type in LOGGER_LEVELS_NORMAL: return logger
    elif type in LOGGER_LEVELS_WARN: return error_logger
    else: error_logger.error(r"Log level doesn't exist")

def userInputMode(keybind):
    while True:
        try:
            # print(">> ", end = "\0")
            user_input = input().split()
            if len(user_input) == 0:
                pass
            elif len(user_input) == 1:
                keybind[user_input[0]]()
            else:
                keybind[user_input[0]](user_input[1:])
        except KeyError:
            error_logger.warn("Unknown command")
        except IndexError:
            error_logger.warn("Wrong number of arguments")
