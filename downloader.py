import os

def download(path, filename):
    os.system(f"wget {path} -O ./audios/{filename}")