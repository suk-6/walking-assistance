from services.classificator import *
from services.detector import *
from services.recognizer import *

import cv2
import time
import logging
import threading
from datetime import datetime
from keyboard import read_key


class app:
    def __init__(self):
        self.services = {"classificator": None, "detector": None, "recognizer": None}
        self.service = None
        self.exit = False

        self.startTime = int(str(datetime.now().timestamp()).split(".")[0])

        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

        self.LOGGER = logging.getLogger()

    def keyCapture(self):
        while True:
            try:
                key = int(read_key())
                self.service = None

                if key == 8:  # key c
                    self.LOGGER.info("classificator")
                    if self.services["classificator"] is None:
                        self.services["classificator"] = classificator(self.LOGGER)
                    self.service = "classificator"

                if key == 2:  # key d
                    self.LOGGER.info("detector")
                    if self.services["detector"] is None:
                        self.services["detector"] = detector(self.LOGGER)
                    self.service = "detector"

                if key == 15:  # key r
                    self.LOGGER.info("recognizer")
                    if self.services["recognizer"] is None:
                        self.services["recognizer"] = recognizer(self.LOGGER)
                    self.service = "recognizer"

                if key == 12:  # key q
                    self.LOGGER.info("exit")
                    self.exit = True

                time.sleep(0.1)
            except Exception as e:
                self.LOGGER.error(e)

    def main(self):
        cap = cv2.VideoCapture(0)

        while True:
            if self.exit:
                break

            now = int(str(datetime.now().timestamp()).split(".")[0])
            _, frame = cap.read()

            if self.service is not None:
                if self.service == "recognizer" and (now - self.startTime) % 3 != 0:
                    continue
                self.services[self.service].run(frame)

        cap.release()
        exit()

    def run(self):
        threading.Thread(target=self.keyCapture, daemon=True).start()
        self.main()


if __name__ == "__main__":
    app().run()
