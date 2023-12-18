from easyocr import Reader


class recognizer:
    def __init__(self, params):
        self.messenger = params["messenger"]
        self.config = params["config"]

        self.reader = Reader(["ko", "en"], gpu=self.config["gpu"])

    def run(self, frame):
        result = self.reader.readtext(frame, detail=0)
        self.messenger.info(result)
