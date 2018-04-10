from gtts import gTTS
from uuid import uuid4
import os
import atexit

from CJKhyperradicals.dir import tmp_path


def client_say(word, lang):
    tts = gTTS(word, lang)
    filename = str(uuid4()) + '.mp3'
    temp_file = tmp_path(filename)
    tts.save(temp_file)

    atexit.register(os.remove, temp_file)

    return filename


if __name__ == '__main__':
    pass
