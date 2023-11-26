from services.classificator import *
from services.detector import *
from services.recognizer import *

from messenger import messenger

import sys
import cv2
import time
import threading
from config import config
from keyboard import read_key


class app:
    def __init__(self):
        self.serviceObjects = {
            "classificator": None,
            "detector": None,
            "recognizer": None,
        }
        self.services = []

        self.cameraStarted = False
        self.isExit = False

        self.messenger = messenger(config)

    def str2class(self, classname):
        return getattr(sys.modules[__name__], classname)

    def switchService(self, *services):
        self.services = []
        self.messenger.info(" ".join(services))
        for service in services:
            if self.serviceObjects[service] is None:
                self.serviceObjects[service] = self.str2class(service)(
                    self.messenger, config
                )
            self.services.append(service)

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
                    self.switchService("classificator", "detector")

                elif key == 2:  # key d
                    self.switchService("detector")

                elif key == 15:  # key r
                    self.switchService("recognizer")

                elif key == 12:  # key q
                    self.exit()

                else:
                    self.messenger.warning("Invalid key")
                    continue

                time.sleep(0.1)
            except Exception as e:
                self.messenger.error(e)

    def main(self):
        self.messenger.info("Starting...")

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["camera"]["width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["camera"]["height"])
        self.cameraStarted = True
        self.messenger.info("Camera started")

        while not self.isExit:
            _, frame = self.cap.read()
            cv2.imshow("Inference", frame)

            if self.services != []:
                for service in self.services:
                    self.serviceObjects[service].run(frame)

    def run(self):
        threading.Thread(target=self.keyCapture, daemon=True).start()
        self.main()

    def exit(self):
        self.isExit = True
        self.cap.release()
        cv2.destroyAllWindows()
        self.messenger.info("exit")
        self.messenger.waitDone(0.1)
        exit()


if __name__ == "__main__":
    app().run()
