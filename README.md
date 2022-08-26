# detection-benchmark

This application is use to evaluate a detection model performance using the metrics AP, AP50, AP75, AR1, AR10, and AR100.

## How it works?

This application will send a POST request for each image to an endpoint. The endpoint is expected to return a JSON containing a list of predicted bounding boxes correspond to the given image with status code 200. Afterwards, the application will calculate the performance of the predictions compared to the ground truth using the metrics AP, AP50, AP75, AR1, AR10, and AR100.

**DISCLAIMER: Metrics calculation is done using [TorchMetrics](https://torchmetrics.readthedocs.io/en/stable/detection/mean_average_precision.html)**

## Dataset

Format of a dataset folder.

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

* The folder `dataset_folder/images/` contains images that will be used to evaluate.

* The folder `dataset_folder/annotations/` contains annotations that will be used as ground truths. Annotation file `<name>.txt` correspond to image `<name>.jpg`. Annotation file is written using the format `<class> <xmin> <ymin> <xmax> <ymax>`. [(See example of an annotation file)](./data/sample/annotations/000001.txt)

* The file `dataset_folder/info.json` contains information about the dataset. [(See example of an info.json)](./data/sample/info.json)

### The PASCAL Visual Object Classes Challenge 2007 Dataset

Run the following command on terminal to run `download_VOC2007.py`, which will download [**PASCAL VOC 2007**](http://host.robots.ox.ac.uk/pascal/VOC/voc2007/index.html) dataset. Downloaded dataset can be founded at the `./data/`.

```bash
python3 download_VOC2007.py
```

## Usage

* [Create An Endpoint](#create-an-endpoint)

* [Evaluation](#evaluation)

* [Evaluation With Provided Prediction Annotations](#evaluation-with-provided-prediction-annotations)

### Create An Endpoint

Since this application will send a POST request for each image to an endpoint, you will need to create a server application to receive a POST request and return a response of a JSON containing a list of predicted bounding boxes correspond to the given image with status code 200. 

JSON response is a list of bounding boxes with the following format.

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

I have also provided a Flask script [`dummy_server.py`](./dummy_server.py), which will serve as dummy endpoint returning random bounding boxes.

Run the following command on terminal to run `dummy_server.py`.

```bash
python3 dummy_server.py --host 0.0.0.0 --port 8000
```

### Evaluation

While server endpoint is running, run the following command on terminal to start the evaluation process.

```bash
python3 evaluate.py \
    --dataset data/sample/ \
    --url http://localhost:8000 \
    --output results/ \
    --title my_first_evaluation \
    --desc "This is the description about my first evaluation experience"
```

This might take a while. Once the evaluation process is done, your model predicted bounding boxes can be found at `./results/title/predictions/` and your evaluation report can be found at `./results/title/report.md`.

### Evaluation With Provided Prediction Annotations

In some case, you might not want to provide an endpoint. In this case, you still can evaluate your detection models by provided a folder contains prediction annotations of your model. Prediction annotation file `<name>.txt` correspond to image `<name>.jpg`. Prediction annotation file is written using the format `<class> <confidence> <xmin> <ymin> <xmax> <ymax>`. [(See example of an prediction annotation file)](./results/sample/predictions/000001.txt)

Then, run the following command to start the evaluation process.

```bash
python3 calculate.py \
    --dataset data/sample/ \
    --predictions predicted_annotations/ \
    --output report.md \
    --title my_first_evaluation \
    --desc "This is the description about my first evaluation experience"
```

Once the evaluation process is done, your evaluation report can be found at `./report.md`.

---

This project was developed as part of thesis project, Computer Science, BINUS University.
