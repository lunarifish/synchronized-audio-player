from pydub import AudioSegment


def clip(path, pos, output_filename):
    def sec(t):
        return t * 1000
    audio = AudioSegment.from_mp3(path)
    audio[sec(pos):].export(output_filename, format = "wav")