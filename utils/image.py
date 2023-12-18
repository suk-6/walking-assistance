class Image:
    def __init__(self) -> None:
        self.imageList = []
        self.lastIndexs = None

    def save(self, image):
        self.imageList.append(image)

        return len(self.imageList) - 1

    def load(self, index):
        return self.imageList[index]

    def saveLastIndex(self, indexs):
        self.lastIndexs = indexs
