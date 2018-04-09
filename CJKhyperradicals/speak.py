from gtts import gTTS
from uuid import uuid4
from tempfile import TemporaryFile
import os
import pygame

from CJKhyperradicals.dir import temp_path


def universal_say(word, lang):
    tts = gTTS(word, lang)
    temp_file = temp_path(str(uuid4()))
    tts.save(temp_file)

    pygame.mixer.init()
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()

    os.remove(temp_file)


if __name__ == '__main__':
    universal_say('hello', 'en-us')

    from time import sleep
    sleep(5)
