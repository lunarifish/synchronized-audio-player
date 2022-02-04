import eyed3
def getLength(filename):
    audio = eyed3.load(f"./audios/{filename}")
    length = int(audio.info.time_secs)
    return length