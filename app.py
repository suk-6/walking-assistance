from services.classificator import *
from services.detector import *
from services.recognizer import *

from messenger import messenger

import cv2
import time
import threading
from config import config
from keyboard import read_key


class app:
    def __init__(self):
        self.services = {"classificator": None, "detector": None, "recognizer": None}
        self.service = None

        self.cameraStarted = False
        self.exit = False

        self.messenger = messenger(config)

    def keyCapture(self):
        while True:
            try:
                key = read_key()
                if type(key) == str:
                    self.messenger.warning("Invalid key")
                    continue

                key = int(key)
                self.service = None

                if self.cameraStarted is False:
                    self.messenger.info("Camera not started")
                    continue

                if key == 8:  # key c
                    self.messenger.info("classificator")
                    if self.services["classificator"] is None:
                        self.services["classificator"] = classificator(
                            self.messenger, config
                        )
                    self.service = "classificator"

                elif key == 2:  # key d
                    self.messenger.info("detector")
                    if self.services["detector"] is None:
                        self.services["detector"] = detector(self.messenger, config)
                    self.service = "detector"

                elif key == 15:  # key r
                    self.messenger.info("recognizer")
                    if self.services["recognizer"] is None:
                        self.services["recognizer"] = recognizer(self.messenger)
                    self.service = "recognizer"

                elif key == 12:  # key q
                    self.messenger.info("exit", force=True)
                    self.exit = True

                else:
                    self.messenger.warning("Invalid key")
                    continue

                time.sleep(0.1)
            except Exception as e:
                self.messenger.error(e)

    def main(self):
        self.messenger.info("Starting...")

        cap = cv2.VideoCapture(0)
        self.cameraStarted = True
        self.messenger.info("Camera started")

        while True:
            if self.exit:
                while self.messenger.isPlaying():
                    pass
                break

            _, frame = cap.read()

            if self.service is not None:
                self.services[self.service].run(frame)

        cap.release()
        exit()

    def run(self):
        threading.Thread(target=self.keyCapture, daemon=True).start()
        self.main()


if __name__ == "__main__":
    app().run()
