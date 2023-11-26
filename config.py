import torchvision.transforms as transforms
from classificatorCNN import CustomClassifier

config = {
    "translate": True,
    "detector": {
        "model": "./models/detector.pt",
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
        "model": "./models/classificator.pth",
        "class": ["road", "wall"],
        "transform": transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize((128, 128)),
                transforms.ToTensor(),
            ]
        ),
        "cnn": CustomClassifier(),
    },
}
