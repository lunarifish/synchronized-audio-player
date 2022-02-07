import wget
import tempfile
import os
import random
import shutil
from variables import *
from console import log
import traceback


dir = tempfile.gettempdir() + "/liveaudio"
if not os.path.exists(dir):
    os.mkdir(dir)

def cleanTempFile():
    if os.path.exists(dir):
        shutil.rmtree(dir)
    else:
        log("warn").warning(r"Temp dictionary doesn't exist")

def download(url):
    try:
        filename = wget.filename_from_url(url)
        path = os.path.join(dir, filename)
        if os.path.exists(path):
            log("warn").warning("File already exists, rename")
            path += str(random.randint(1, 100000))
        log().info(f"Downloading into file: {path}")
        wget.download(url, out = path)
        log().info(f"Saved to file {path}")
        return path
    except:
        set("code", 1)
        return None
        for i in traceback.format_exc().split("\n"):
            log("error").error(i)