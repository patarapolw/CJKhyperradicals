from gtts import gTTS
from tempfile import TemporaryFile
import base64
from uuid import uuid4
import os
import atexit


class Tts:
    def __init__(self, word, lang):
        self.tts = gTTS(word, lang)

    def to_temp(self, temp: str=None):
        if temp is None:
            temp = os.path.join('tmp', str(uuid4()) + '.mp3')

        atexit.register(os.remove, temp)
        self.to_file(temp)

        return temp

    def to_file(self, filename):
        self.tts.save(filename)

        return filename

    def to_bytes(self):
        # temp = TemporaryFile()
        # self.tts.write_to_fp(temp)
        # print(temp.read())
        #
        # return temp.read()
        with open(self.to_temp(), 'rb') as f:
            return f.read()

    def to_base64(self):
        return base64.b64encode(self.to_bytes())


if __name__ == '__main__':
    print(Tts('你好', 'zh-cn').to_base64())
