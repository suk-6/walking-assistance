import cv2
import threading


class Image:
    def __init__(self) -> None:
        self.imageList = []
        self.lastIndexs = []

    def save(self, image):
        self.imageList.append(image)

        return len(self.imageList) - 1

    def load(self, index):
        image = self.imageList[index]
        self.remove(index)
        return image

    def saveLastIndex(self, indexs):
        self.lastIndexs = indexs
        # threading.Timer(10, self.clear).start()

    def getLastIndex(self):
        return self.lastIndexs

    def remove(self, index):
        image = self.imageList[index]
        self.imageList.remove(image)
        self.lastIndexs.remove(index)

    def clear(self):
        self.imageList = []
        self.lastIndexs = []
