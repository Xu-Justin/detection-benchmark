import os
import json

class Dataset:
    max_repr_index = 8

    def __init__(self, folder):
        self.load_dataset(folder)
    
    def __repr__(self):
        return (
            f"dataset_name   : {self.dataset_name}\n"
            f"folder         : {self.folder}\n"
            f"num_of_classes : {self.num_of_classes}\n"
            f"classes        : {self.classes[:min(self.max_repr_index, len(self.classes))]}\n"
            f"num_of_images  : {self.num_of_images}\n"
            f"images         : {self.images[:min(self.max_repr_index, len(self.images))]}\n"
            f"object         : {super().__repr__()}\n"
        )

    def load_dataset(self, folder):
        self.folder = folder
        
        with open(os.path.join(folder, "info.json"), "r") as f:
            data = json.load(f)
        
        self.dataset_name = data['dataset_name']
        self.num_of_classes = data['num_of_classes']
        self.classes = data['classes']
        self.num_of_images = data['num_of_images']
        self.images = data['images']

        self.validate()

    def validate(self, folder_predictions=None):
        assert self.num_of_classes == len(self.classes), f"Not match num_of_classes {self.num_of_classes} with len(classes) {len(self.classes)}"
        assert self.num_of_images == len(self.images), f"Not match num_of_images {self.num_of_images} with len(images) {len(self.images)}"

        folder_images = os.path.join(self.folder, 'images')
        images = os.listdir(folder_images)
        assert sorted(self.images) == sorted(images), f"Not match images with files in {folder_images}"
        
        def strip_ext(file_name):
            index = file_name.rindex('.')
            return file_name[:index]

        folder_annotations = os.path.join(self.folder, 'annotations')
        annotations = os.listdir(folder_annotations)
        assert sorted(list(map(strip_ext, self.images))) == sorted(list(map(strip_ext, annotations))), f"Not match annotations with files in {folder_annotations}"

        if folder_predictions is not None:
            predictions = os.listdir(folder_predictions)
            assert sorted(list(map(strip_ext, self.images))) == sorted(list(map(strip_ext, predictions))), f"Not match annotations with files in {folder_predictions}"
