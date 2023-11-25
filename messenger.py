import os
import inspect
import logging
from glob import glob
from io import BytesIO

from gtts import gTTS
from string import punctuation
from pydub import AudioSegment
from pydub.playback import play

from labels import printLabels


class messenger:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

        self.LOGGER = logging.getLogger()

    def info(self, msg):
        caller = inspect.currentframe().f_back.f_globals["__name__"]
        if caller == "__main__":
            caller = "main"
        else:
            caller = caller.split(".")[-1]

        self.LOGGER.info(msg)
        self.say(msg, caller)

    def error(self, msg):
        self.LOGGER.error(msg)

    def say(self, msg, caller):
        if caller == "main":
            self.tts(msg)

        elif caller == "detector":
            for data in msg:
                if data["labelName"] in printLabels:
                    self.tts(f"{data['labelName']} {data['position']}")

        elif caller == "recognizer":
            if msg == []:
                return

            en = ""
            ko = ""

            for data in msg:
                for char in data:
                    if char not in punctuation:
                        if char.encode().isalpha():
                            en += char
                        else:
                            ko += char
                en += " "
                ko += " "

            if en.strip() != "":
                self.tts(en, "en")

            if ko.strip() != "":
                self.tts(ko, "ko")

    def tts(self, msg, lang="en"):
        tts = gTTS(text=msg, lang=lang)

        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        song = AudioSegment.from_file(fp, format="mp3")
        play(song)

        fileList = glob("./ffcache*")
        for filePath in fileList:
            os.remove(filePath)
