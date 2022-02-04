from audio import getLength
from downloader import download
import time
from threading import Thread
from server import getSongPos
from server import changeSong
import variables
import sys

variables._init()
variables.set("isplaying", 0)
variables.set("songurl", "none")
variables.set("songpos", "none")
variables.set("stop", 0)
variables.set("server_port", int(sys.argv[1]))
variables.set("controller_port", int(sys.argv[2]))

def updatePos():
    starttime = time.time()
    song_len = 0
    pos = 0
    print("(TIMING THREAD)Timing thread started")
    while variables.get("stop") == 0:
        try:
            print(f"(TIMING THREAD)Playing: {pos}/{song_len}")
            time.sleep(0.7)
            if variables.get("onChange") == 1:
                songurl = variables.get("songurl")
                download(songurl, "song.mp3")
                print("Download finished")
                song_len = getLength("song.mp3")
                starttime = time.time()
                variables.set("onChange", 0)
                variables.set("code", 0)
            else:
                pos = int(time.time() - starttime)
                variables.set("songpos", pos)
            if pos > song_len:
                pos = song_len
        except:
            variables.set("code", 1)


thread_timing = Thread(target = updatePos, name = "timing")
thread_server = Thread(target = getSongPos, name = "server")
thread_controller = Thread(target = changeSong, name = "controller")
try:
    thread_timing.start()
    thread_server.start()
    thread_controller.start()
except:
    pass
while True:
    command = input()
    if command == "q":
        print("Server stoping")
        variables.set("stop", 1)
        thread_timing.join()
        thread_server.join()
        thread_controller.join()
        sys.exit()
