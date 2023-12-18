import cv2
import torch


class classificator:
    def __init__(self, params):
        self.messenger = params["messenger"]
        self.config = params["config"]

        self.transform = self.config["classificator"]["transform"]

        if torch.cuda.is_available() and self.config["gpu"]:
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available() and self.config["gpu"]:
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")

        self.messenger.logger().info(f"Device: {self.device}")

        self.model = self.config["classificator"]["cnn"]
        self.model.load_state_dict(
            torch.load(self.config["classificator"]["model"], map_location=self.device)
        )

        self.model.eval()

    def getPrediction(self, frame):
        with torch.no_grad():
            output = self.model(frame)
            return torch.sigmoid(output).item()

    def run(self, frame):
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = self.transform(frame).unsqueeze(0)

            prediction = self.getPrediction(frame)
            if prediction > 0.5:
                self.messenger.info(self.config["classificator"]["class"][1])

        except Exception as e:
            self.messenger.error(e)
