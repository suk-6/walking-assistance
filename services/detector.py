import torch
import cv2


class detector:
    def __init__(self, params):
        self.messenger = params["messenger"]
        self.config = params["config"]
        self.image = params["image"]
        self.model = torch.hub.load(
            "./yolov5",
            "custom",
            path=self.config["detector"]["model"],
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

    def imageSaver(self, frame, results):
        indexs = []

        for result in results:
            if result["labelName"] in self.config["saveBoxes"]:
                imageWidth = result["imageWidth"]
                imageHeight = result["imageHeight"]

                left = int(result["left"] * imageWidth)
                top = int(result["top"] * imageHeight)
                width = int(result["width"] * imageWidth)
                height = int(result["height"] * imageHeight)

                cropped = frame[top : top + height, left : left + width]
                index = self.image.save(cropped)
                indexs.append(index)

                self.messenger.warning(f"{result['labelName']}", tell=True)

        if indexs != []:
            self.image.saveLastIndex(indexs)

    def run(self, frame, dual=False):
        self.dual = dual
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
        self.imageSaver(frame, results)

        self.messenger.info(results, force=self.dual)
