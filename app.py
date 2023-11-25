from services.classificator import *
from services.detector import *
from services.recognizer import *

from messenger import messenger

import cv2
import time
import threading
from datetime import datetime
from keyboard import read_key


class app:
    def __init__(self):
        self.services = {"classificator": None, "detector": None, "recognizer": None}
        self.service = None
        self.exit = False

        self.messenger = messenger()

    def keyCapture(self):
        while True:
            try:
                key = int(read_key())
                self.service = None

                if key == 8:  # key c
                    self.messenger.info("classificator")
                    if self.services["classificator"] is None:
                        self.services["classificator"] = classificator(self.messenger)
                    self.service = "classificator"

                if key == 2:  # key d
                    self.messenger.info("detector")
                    if self.services["detector"] is None:
                        self.services["detector"] = detector(self.messenger)
                    self.service = "detector"

                if key == 15:  # key r
                    self.messenger.info("recognizer")
                    if self.services["recognizer"] is None:
                        self.services["recognizer"] = recognizer(self.messenger)
                    self.service = "recognizer"

                if key == 12:  # key q
                    self.messenger.info("exit")
                    self.exit = True

                time.sleep(0.1)
            except Exception as e:
                self.messenger.error(e)

    def main(self):
        self.messenger.info("Starting...")

        cap = cv2.VideoCapture(0)
        self.messenger.info("Camera started")

        while True:
            if self.exit:
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
