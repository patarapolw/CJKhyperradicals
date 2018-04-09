from gtts import gTTS
from uuid import uuid4
from pydub import AudioSegment
import os
import simpleaudio as sa

from CJKhyperradicals.dir import temp_path


def universal_say(word, lang):
    tts = gTTS('hello', 'en-us')
    temp_file = temp_path(str(uuid4()))
    tts.save(temp_path(temp_file))

    AudioSegment.from_mp3(temp_file).export(temp_file, 'wav')
    wave_obj = sa.WaveObject.from_wave_file(temp_file)
    play_obj = wave_obj.play()
    play_obj.wait_done()

    os.remove(temp_file)
