import torch


class detector:
    def __init__(self, messenger, config):
        self.messenger = messenger
        self.config = config
        self.model = torch.hub.load(
            "./yolov5",
            "custom",
            path=config["detector"]["model"],
            source="local",
            force_reload=True,
        )

    def resultParser(self, params):
        imageWidth = params["image"]["width"]
        imageHeight = params["image"]["height"]
        imageArea = params["image"]["area"]
        results = params["results"]

        annos = []

        for bbox in zip(results.xyxy[0]):
            xmin, ymin, xmax, ymax, conf, label = bbox[0].tolist()

            relativeXmin = xmin / imageWidth
            relativeYmin = ymin / imageHeight
            relativeWidth = (xmax - xmin) / imageWidth
            relativeHeight = (ymax - ymin) / imageHeight

            bboxCoords = {
                "imageWidth": imageWidth,
                "imageHeight": imageHeight,
                "left": relativeXmin,
                "top": relativeYmin,
                "width": relativeWidth,
                "height": relativeHeight,
                "conf": conf,
                "label": int(label),
                "position": -1,
                "ratio": -1,
            }

            xCenter = (xmin + xmax) / 2
            imageSplit = imageWidth / 3

            if xCenter < imageSplit:
                bboxCoords["position"] = "left"
            elif xCenter < imageSplit * 2:
                bboxCoords["position"] = "center"
            elif xCenter < imageSplit * 3:
                bboxCoords["position"] = "right"
            else:
                bboxCoords["position"] = -1

            # 바운딩 박스의 크기 비율 계산
            bboxWidth = xmax - xmin
            bboxHeight = ymax - ymin
            bboxArea = bboxWidth * bboxHeight
            bboxRatio = (bboxArea / imageArea) * 100  # 퍼센트로 표현

            bboxCoords["ratio"] = bboxRatio
            bboxCoords["labelName"] = self.config["detector"]["labels"][int(label)]

            annos.append(bboxCoords)

        return annos

    def run(self, frame):
        results = self.model(frame)

        params = {
            "image": {
                "width": frame.shape[1],
                "height": frame.shape[0],
                "area": frame.shape[1] * frame.shape[0],
            },
            "results": results,
        }

        results = self.resultParser(params)

        self.messenger.info(results)
