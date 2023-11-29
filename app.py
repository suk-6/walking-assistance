from services.classificator import *
from services.detector import *
from services.recognizer import *

from messenger import messenger

import sys
import cv2
import time
import threading
from config import configLoader
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

        self.config = configLoader().getConfig()

        self.messenger = messenger(self.config)

    def str2class(self, classname):
        return getattr(sys.modules[__name__], classname)

    def switchService(self, *services):
        self.services = []
        self.messenger.info(" ".join(services))
        for service in services:
            if self.serviceObjects[service] is None:
                self.serviceObjects[service] = self.str2class(service)(
                    self.messenger, self.config
                )
            self.services.append(service)

    def keyCapture(self):
        while True:
            try:
                key = read_key()
                self.service = None

                if self.cameraStarted is False:
                    self.messenger.info("Camera not started")
                    continue

                if key == self.config["key"]["c"]:  # key c
                    self.switchService("classificator", "detector")

                elif key == self.config["key"]["d"]:  # key d
                    self.switchService("detector")

                elif key == self.config["key"]["r"]:  # key r
                    self.switchService("recognizer")

                elif key == self.config["key"]["q"]:  # key q
                    self.exit()

                else:
                    self.messenger.warning("Invalid key")
                    continue

                time.sleep(0.1)
            except Exception as e:
                self.messenger.error(e)

    def main(self):
        self.messenger.info("Starting...")

        self.cap = cv2.VideoCapture(self.config["camera"]["device"])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config["camera"]["width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config["camera"]["height"])
        self.cameraStarted = True
        self.messenger.info("Camera started")

        while not self.isExit:
            _, frame = self.cap.read()
            cv2.imshow("Live View", frame)
            cv2.waitKey(1)

            if self.services != []:
                for service in self.services:
                    self.serviceObjects[service].run(frame)

    def run(self):
        threading.Thread(target=self.keyCapture).start()
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
