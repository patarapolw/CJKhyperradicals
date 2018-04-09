from gtts import gTTS
from uuid import uuid4
import subprocess
import os

from CJKhyperradicals.dir import temp_path


tts = gTTS('hello', 'en-us')
temp_file = str(uuid4())
tts.save(temp_path(temp_file))

subprocess.call(['ffplay', "-nodisp", "-autoexit", temp_path(temp_file)])
os.remove(temp_path(temp_file))
