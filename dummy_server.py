import cv2
import json
import numpy as np
from flask import Flask, request, Response

def get_args_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    return args

app = Flask(__name__)

@app.route('/', methods=['POST'])
def response():
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    def random_bbox(image):
        height, width, channels = image.shape
        
        xmin, xmax = np.random.randint(1, width+1, 2)
        if xmin > xmax: xmin, xmax = xmax, xmin
        ymin, ymax = np.random.randint(1, height+1, 2)
        if ymin > ymax: ymin, ymax = ymax, ymin

        class_name = np.random.choice([
            "aeroplane",
            "bicycle",
            "bird",
            "boat",
            "bottle",
            "bus",
            "car",
            "cat",
            "chair",
            "cow",
            "diningtable",
            "dog",
            "horse",
            "motorbike",
            "person",
            "pottedplant",
            "sheep",
            "sofa",
            "train",
            "tvmonitor"
        ])
        confidence = np.random.rand()

        return class_name, confidence, xmin, ymin, xmax, ymax

    bounding_boxes = []
    for i in range(20):
        class_name, confidence, xmin, ymin, xmax, ymax = random_bbox(image)
        if confidence > 0.5: bounding_boxes.append({
            'class': str(class_name),
            'confidence': float(confidence),
            'xmin': int(xmin),
            'ymin': int(ymin),
            'xmax': int(xmax),
            'ymax': int(ymax)
        }) 

    response = json.dumps(bounding_boxes)
    return Response(response=response, status=200, mimetype="application/json")

def main(args):
    app.run(args.host, args.port, debug=False)

if __name__ == '__main__':
    args = get_args_parser()
    print(args)
    main(args)
