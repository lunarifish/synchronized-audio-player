import os
from console import log

def download(path, filename):
    os.system(f"wget {path} -O ./audios/{filename}")