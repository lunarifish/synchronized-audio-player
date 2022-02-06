import threading

def log(*message):
    print(f"({threading.currentThread().name})" + " ".join(message))

def userInputMode(keybind):
    while True:
        try:
            print(">> ", end = "\0")
            user_input = input().split()
            if len(user_input) == 0:
                pass
            elif len(user_input) == 1:
                keybind[user_input[0]]()
            else:
                keybind[user_input[0]](user_input[1:])
        except KeyError:
            log("Unknown command")
        except IndexError:
            log("Wrong number of arguments")