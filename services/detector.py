import torch


class detector:
    def __init__(self, LOGGER):
        self.LOGGER = LOGGER
        self.model = torch.hub.load(
            "./yolov5",
            "custom",
            path="./models/detector.pt",
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
                bboxCoords["position"] = 0  # 왼쪽
            elif xCenter < imageSplit * 2:
                bboxCoords["position"] = 1  # 중앙
            elif xCenter < imageSplit * 3:
                bboxCoords["position"] = 2  # 오른쪽
            else:
                bboxCoords["position"] = -1

            # 바운딩 박스의 크기 비율 계산
            bboxWidth = xmax - xmin
            bboxHeight = ymax - ymin
            bboxArea = bboxWidth * bboxHeight
            bboxRatio = (bboxArea / imageArea) * 100  # 퍼센트로 표현

            bboxCoords["ratio"] = bboxRatio

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

        self.LOGGER.info(results)
