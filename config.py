import os
import time
import pickle
from pprint import pprint
from typing import Any
from keyboard import read_key
import torchvision.transforms as transforms
from classificatorCNN import CustomClassifier


class configLoader:
    def __init__(self):
        self.root = os.getcwd()
        self.config = {
            "translate": True,
            "gpu": False,
            "camera": {
                "device": 0,
                "width": 256,
                "height": 256,
            },
            "key": {},
            "detector": {
                "model": os.path.join(self.root, "models", "detector.pt"),
                "labels": [
                    "tree",
                    "car",
                    "person",
                    "pole",
                    "fence",
                    "utility_pole",
                    "bollard",
                    "bicycle",
                    "motorcycle",
                    "flower_bed",
                    "dog",
                    "bus_stop",
                    "traffic_cone",
                    "truck",
                    "bench",
                    "bus",
                    "kickboard",
                    "streetlamp",
                    "telephone_booth",
                    "trash",
                    "fire_plug",
                    "plant",
                    "sign_board",
                    "fire_hydrant",
                    "corner",
                    "opened_door",
                    "mailbox",
                    "unknown",
                    "banner",
                ],
                "printLabels": [
                    "person",
                    "bollard",
                    "bicycle",
                    "motorcycle",
                    "traffic_cone",
                    "kickboard",
                ],
            },
            "classificator": {
                "model": os.path.join(self.root, "models", "classificator.pth"),
                "class": ["road", "wall"],
                "transform": transforms.Compose(
                    [
                        transforms.ToPILImage(),
                        transforms.Resize((128, 128)),
                        transforms.ToTensor(),
                        transforms.Normalize(
                            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                        ),
                    ]
                ),
                "cnn": CustomClassifier(),
            },
            "saveBoxes": ["sign_board"],
        }

        if self.configLoad() is False:
            self.configSettings()
            self.configSave()

    def getConfig(self):
        pprint(self.config)
        return self.config

    def configSettings(self):
        self.keySettings()
        self.garbege()
        self.cameraSettings()
        self.gpuSettings()
        self.garbege()

    def configLoad(self):
        if os.path.exists("config.pickle"):
            with open("config.pickle", "rb") as file:
                self.config = pickle.load(file)
                return True
        return False

    def configSave(self):
        with open("config.pickle", "wb") as file:
            pickle.dump(self.config, file)

    def garbege(self):
        input("\nPress 'Enter' key to continue...")

    def keySettings(self):
        for key in ["c", "d", "r", "q"]:
            print(f"\nPress '{key}' to switch classificator and detector")
            self.config["key"][key] = read_key()
            time.sleep(0.2)

    def cameraSettings(self):
        print("\nCamera settings")
        self.config["camera"]["device"] = int(input("Camera device: "))

    def gpuSettings(self):
        print("\nGPU settings")
        confirm = input("Use GPU? (y/N): ")
        if confirm == "y":
            self.config["gpu"] = True
        else:
            self.config["gpu"] = False
