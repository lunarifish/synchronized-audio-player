import eyed3
import time
from downloader import download
from console import log
import variables

def getLength(filename):
    audio = eyed3.load(f"./audios/{filename}")
    length = int(audio.info.time_secs)
    return length

def updatePos():
    starttime = time.time()
    song_len = 0
    pos = 0
    print("Timing thread started")
    while variables.get("stop") == 0:
        try:
            time.sleep(0.7)
            if variables.get("onChange") == 1:
                songurl = variables.get("songurl")
                download(songurl, "song.mp3")
                song_len = getLength("song.mp3")
                variables.set("songlen", song_len)
                starttime = time.time()
                variables.set("onChange", 0)
                variables.set("code", 0)
                log(f"New timer: 0/{song_len}")
            else:
                pos = int(time.time() - starttime)
                variables.set("songpos", pos)
            if pos > song_len:
                pos = song_len
                variables.set("songpos", pos)
        except:
            variables.set("code", 1)
    log("Timing thread stoping")