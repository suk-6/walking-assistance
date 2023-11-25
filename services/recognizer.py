from easyocr import Reader


class recognizer:
    def __init__(self, messenger):
        self.messenger = messenger
        self.reader = Reader(["ko", "en"], gpu=False)

    def run(self, frame):
        result = self.reader.readtext(frame, detail=0)
        self.messenger.info(result)
