from server import sendData
import audio as au
from wget import download
import time
import os
import winsound


HOST = "siyfico.cloud"
PORT = 10109
DLPATH = "./audio.mp3"
OUTPATH = "audio_processed.wav"
while int(sendData(HOST, PORT, "isplaying")) != 1:
    pass
song = sendData(HOST, PORT, "url")

download(song, DLPATH)
time.sleep(0.5)
song_pos = int(sendData(HOST, PORT, "songpos"))
au.clip(DLPATH, song_pos, OUTPATH)
os.remove(DLPATH)

player = winsound.PlaySound(None, winsound.SND_NODEFAULT)

def player_start():
    global player
    player = winsound.PlaySound(OUTPATH, winsound.SND_ASYNC)

def player_stop():
    global player
    winsound.PlaySound(player, winsound.SND_PURGE)

player_start()
while True:
    time.sleep(2)
    if song != sendData(HOST, PORT, "url"):
        player_stop()
        song = sendData(HOST, PORT, "url")
        download(song, DLPATH)
        time.sleep(2)
        song_pos = int(sendData(HOST, PORT, "songpos"))
        au.clip(DLPATH, song_pos, OUTPATH)
        os.remove(DLPATH)
        player_start()
