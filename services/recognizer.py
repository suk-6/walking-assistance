from easyocr import Reader


class recognizer:
    def __init__(self, LOGGER):
        self.LOGGER = LOGGER
        self.reader = Reader(["ko", "en"], gpu=False)

    def run(self, frame):
        result = self.reader.readtext(frame, detail=0)
        self.LOGGER.info(result)
