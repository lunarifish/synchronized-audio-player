from pydub import AudioSegment


def clip(path, pos, output_filename):
    def sec2ms(t):
        return t * 1000
    audio = AudioSegment.from_mp3(path)
    audio[sec2ms(pos):].export(output_filename, format = "wav")
