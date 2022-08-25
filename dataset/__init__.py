import os
import json
import torch
from torchmetrics.detection.mean_ap import MeanAveragePrecision

from utils import strip_ext

class Dataset:
    MAX_REPR_INDEX = 8

    RPATH_FOLDER_IMAGES = 'images'
    RPATH_FOLDER_ANNOTATIONS = 'annotations'
    RPATH_INFO = 'info.json'

    INDEX_dataset_name = 'dataset_name'
    INDEX_num_of_classes = 'num_of_classes'
    INDEX_classes = 'classes'
    INDEX_num_of_images = 'num_of_images'
    INDEX_images = 'images'

    EXT_ANNOTATION = '.txt'

    def __init__(self, folder):
        self.load_dataset(folder)
    
    def __repr__(self):
        return (
            f"dataset_name   : {self.dataset_name}\n"
            f"folder         : {self.folder}\n"
            f"num_of_classes : {self.num_of_classes}\n"
            f"classes        : {self.classes[:min(self.MAX_REPR_INDEX, len(self.classes))]}{' (truncated)' if len(self.classes) > self.MAX_REPR_INDEX else ''}\n"
            f"num_of_images  : {self.num_of_images}\n"
            f"images         : {self.images[:min(self.MAX_REPR_INDEX, len(self.images))]}{' (truncated)' if len(self.images) > self.MAX_REPR_INDEX else ''}\n"
            f"object         : {super().__repr__()}\n"
        )

    def load_dataset(self, folder):
        assert os.path.exists(folder), f"Folder {folder} don't exists"

        self.folder = folder
        self.folder_images = os.path.join(self.folder, self.RPATH_FOLDER_IMAGES)
        self.folder_annotations = os.path.join(self.folder, self.RPATH_FOLDER_ANNOTATIONS)
        
        with open(os.path.join(folder, self.RPATH_INFO), "r") as f:
            data = json.load(f)
        
        self.dataset_name = data[self.INDEX_dataset_name]
        self.num_of_classes = data[self.INDEX_num_of_classes]
        self.classes = data[self.INDEX_classes]
        self.num_of_images = data[self.INDEX_num_of_images]
        self.images = data[self.INDEX_images]

        self.validate()

    def validate(self, folder_predictions=None):
        assert self.num_of_classes == len(self.classes), f"Not match num_of_classes {self.num_of_classes} with len(classes) {len(self.classes)}"
        assert self.num_of_images == len(self.images), f"Not match num_of_images {self.num_of_images} with len(images) {len(self.images)}"

        images = os.listdir(self.folder_images)
        assert sorted(self.images) == sorted(images), f"Not match images with files in {self.folder_images}"
        
        annotations = os.listdir(self.folder_annotations)
        assert sorted(list(map(strip_ext, self.images))) == sorted(list(map(strip_ext, annotations))), f"Not match annotations with files in {self.folder_annotations}"

        if folder_predictions is not None:
            predictions = os.listdir(folder_predictions)
            assert sorted(list(map(strip_ext, self.images))) == sorted(list(map(strip_ext, predictions))), f"Not match annotations with files in {folder_predictions}"

    def get_image_path(self, index):
        return os.path.join(self.folder_images, self.images[index])

    def get_annotation_file_name(self, image_file_name):
        return strip_ext(image_file_name) + self.EXT_ANNOTATION

    def load_annotation_ground_truth(self, path):
        assert os.path.exists(path), f"Path ground truth {path} don't exists"

        boxes = []
        labels = []

        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                class_name, xmin, ymin, xmax, ymax = line.split()
                class_id = self.classes.index(class_name)
                xmin, ymin, xmax, ymax = list(map(float, [xmin, ymin, xmax, ymax]))
                class_id = int(class_id)
                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(class_id)
        
        return dict(
            boxes = torch.tensor(boxes, dtype=torch.float),
            labels = torch.tensor(labels, dtype=torch.int)
        )

    def load_annotations_ground_truth(self):
        assert os.path.exists(self.folder_annotations), f"Folder ground truths {self.folder_annotations} don't exists"

        ground_truths = []
        for image_file_name in self.images:
            annotation_path = os.path.join(self.folder_annotations, self.get_annotation_file_name(image_file_name))
            ground_truth = self.load_annotation_ground_truth(annotation_path)
            ground_truths.append(ground_truth)
        return ground_truths

    def load_annotation_prediction(self, path):
        assert os.path.exists(path), f"Path prediction {path} don't exists"

        boxes = []
        scores = []
        labels = []

        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                class_name, score, xmin, ymin, xmax, ymax = line.split()
                class_id = self.classes.index(class_name)
                xmin, ymin, xmax, ymax = list(map(float, [xmin, ymin, xmax, ymax]))
                score = float(score)
                class_id = int(class_id)
                boxes.append([xmin, ymin, xmax, ymax])
                scores.append(score)
                labels.append(class_id)
        
        return dict(
            boxes = torch.tensor(boxes, dtype=torch.float),
            scores = torch.tensor(scores, dtype=torch.float),
            labels = torch.tensor(labels, dtype=torch.int)
        )

    def load_annotations_predictions(self, folder_predictions):
        assert os.path.exists(folder_predictions), f"Folder predictions {folder_predictions} don't exists"

        predictions = []
        for image_file_name in self.images:
            annotation_path = os.path.join(folder_predictions, self.get_annotation_file_name(image_file_name))
            prediction = self.load_annotation_prediction(annotation_path)
            predictions.append(prediction)
        return predictions
        
    def calculate_mAP(self, folder_predictions):
        ground_truths = self.load_annotations_ground_truth()
        predictions = self.load_annotations_predictions(folder_predictions)
        
        metric = MeanAveragePrecision()
        metric.update(predictions, ground_truths)
        return metric.compute()
