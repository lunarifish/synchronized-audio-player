import eyed3
import time
from file import download
from console import log
import variables
import traceback

def getLength(path):
    try:
        audio = eyed3.load(path)
        length = int(audio.info.time_secs)
        return length
    except AttributeError:
        log("error").error("Target file is not a valid audio file")
        return None
    

def updatePos():
    starttime = time.time()
    song_len = 0
    pos = 0
    log().info("Timing thread started")
    while not variables.get("stop"):
        try:
            time.sleep(0.7)
            if variables.get("onChange") == 1:
                url = variables.get("url")
                file_path = download(url)
                song_len = getLength(file_path)
                variables.set("songlen", song_len)
                starttime = time.time()
                variables.set("onChange", 0)
                variables.set("code", 0)
                log().info(f"New timer: 0/{song_len}")
            else:
                pos = int(time.time() - starttime)
                variables.set("songpos", pos)
            if pos > song_len:
                pos = song_len
                variables.set("songpos", pos)
        except:
            variables.set("code", 1)
            for i in traceback.format_exc().split("\n"):
                log("error").error(i)
    log().info("Thread stopping")