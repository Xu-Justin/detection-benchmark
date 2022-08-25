# detection-benchmark

An application to evaluate a detection model performance.

## How it works?

This application will load a dataset, then send a POST request for each image to an endpoint. The endpoint is expected to return bounding boxes for given image. After all images is sent, the application will evaluate the results using the metrics AP, AP50, AP75, AR1, AR10, and AR100.

## Dataset

Dataset must have the following format

```
dataset_folder
 ├─ images
 |   ├─ 001.jpg
 |   └─ 002.jpg
 ├─ annotations
 |   ├─ 001.txt
 |   └─ 002.txt
 └─ info.json
```

Annotation file `<name>.txt` correspond to image `<name>.jpg`, with annotation format as follows.

```
<class> <xmin> <ymin> <xmax> <ymax>
```

**`info.json`**

```json
{
    "dataset_name" : "sample",
    "num_of_classes" : 3,
    "classes" : [
        "class_A",
        "class_B",
        "class_C"
    ],
    "num_of_images" : 2,
    "images" : [
        "001.jpg",
        "002.jpg"
    ]
}
```

Run the following command to run `download_VOC2007.py`, which will download [**PASCAL VOC 2007**](http://host.robots.ox.ac.uk/pascal/VOC/voc2007/index.html) dataset and convert them.

```bash
python3 download_VOC2007.py
```

## Usage

First, you need to provide an endpoint to receive a POST request and the endpoint is expected to return a JSON corresponds to the given image.

JSON response is a list of bounding box with the following format.

```
[
    {
        "class": str,
        "confidence": float,
        "xmin": int,
        "ymin": int,
        "xmax": int,
        "ymax": int
    }
]
```

Run the following command to run `dummy_server.py`, which will serve as dummy endpoint returning random bounding boxes.

```bash
python3 dummy_server.py --host 0.0.0.0 --port 8000
```

While your server endpoint is running, run the following command to run `evaluate.py`, which will start the evaluation process.

```bash
python3 evaluate.py
    --dataset data/sample/
    --url http://localhost:8000
    --output ./results
    --title my_first_evaluation
    --desc "This is the description about my first evaluation experience"
```

This might take a while. Afterwards, the evaluation report can be found at `./results/title/report.md`.

---

This project was developed as part of thesis project, Computer Science, BINUS University.
