import os    
import shutil
import datetime
import json
from utils import convert_pascal_annotations
from dataset import Dataset
from tqdm import tqdm

RPATH_FOLDER_IMAGES = 'images'
RPATH_FOLDER_ANNOTATIONS = 'annotations'
RPATH_FOLDER_ANNOTATIONS_XML = 'annotations_xml'
RPATH_INFO = 'info.json'

EXT_IMAGE = '.jpg'
EXT_ANNOTATION = '.txt'
EXT_ANNOTATION_XML = '.xml'

voc_classes = [
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
]

def create_structure(folder):
    os.makedirs(folder)
    os.makedirs(os.path.join(folder, RPATH_FOLDER_IMAGES))
    os.makedirs(os.path.join(folder, RPATH_FOLDER_ANNOTATIONS))
    os.makedirs(os.path.join(folder, RPATH_FOLDER_ANNOTATIONS_XML))
    
def create_dataset(dataset_name, temp_text, temp_folder_images, temp_folder_annotations, folder):
    with open(temp_text, "r") as f:
        lines = f.readlines()
        for line in tqdm(lines, desc=dataset_name):
            line = line.strip()
            image_file_name = line + EXT_IMAGE
            image_path = os.path.join(temp_folder_images, image_file_name)
            annotation_file_name = line + EXT_ANNOTATION_XML
            annotation_path = os.path.join(temp_folder_annotations, annotation_file_name)
            
            os.system(f'cp {image_path} {os.path.join(folder, RPATH_FOLDER_IMAGES)}')
            os.system(f'cp {annotation_path} {os.path.join(folder, RPATH_FOLDER_ANNOTATIONS_XML)}')
            convert_pascal_annotations(annotation_path, os.path.join(folder, RPATH_FOLDER_ANNOTATIONS, line + EXT_ANNOTATION))

    # create info.json
    
    images = os.listdir(os.path.join(folder, RPATH_FOLDER_IMAGES))

    info = {
        "dataset_name" : dataset_name,
        "num_of_classes" : len(voc_classes),
        "classes" : voc_classes,
        "num_of_images" : len(images),
        "images" : images
    }

    with open(os.path.join(folder, RPATH_INFO), "w") as f:
        f.write(json.dumps(info, indent=4))

def main():
    root = os.getcwd()
    time = datetime.datetime.now()
    temp_folder = os.path.join(root, f"{time.year}-{time.month}-{time.day}-{time.hour}-{time.minute}-{time.second}-temp-voc2007")
    
    os.makedirs(temp_folder)

    try:
        os.chdir(temp_folder)

        print("Downloading dataset...")
        os.system('wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar')
        os.system('wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar')
        
        print("Extracting dataset...")
        os.system('tar -xf VOCtrainval_06-Nov-2007.tar')
        os.system('tar -xf VOCtest_06-Nov-2007.tar')
        
        os.chdir(root)

        folder_dataset = os.path.join(root, 'data')    
        folder_voc2007_train = os.path.join(folder_dataset, 'voc2007-train')
        folder_voc2007_val = os.path.join(folder_dataset, 'voc2007-val')
        folder_voc2007_test = os.path.join(folder_dataset, 'voc2007-test')

        create_structure(folder_voc2007_train)
        create_structure(folder_voc2007_val)
        create_structure(folder_voc2007_test)

        temp_folder_voc2007 = os.path.join(temp_folder, 'VOCdevkit', 'VOC2007')
        temp_folder_images = os.path.join(temp_folder_voc2007, 'JPEGImages')
        temp_folder_annotations = os.path.join(temp_folder_voc2007, 'Annotations')
        temp_folder_main = os.path.join(temp_folder_voc2007, 'ImageSets', 'Main')
        temp_train_text = os.path.join(temp_folder_main, 'train.txt')
        temp_val_text = os.path.join(temp_folder_main, 'val.txt')
        temp_test_text = os.path.join(temp_folder_main, 'test.txt')
        
        print("Converting dataset format...")
        create_dataset("VOC2007-train", temp_train_text, temp_folder_images, temp_folder_annotations, folder_voc2007_train)
        create_dataset("VOC2007-val", temp_val_text, temp_folder_images, temp_folder_annotations, folder_voc2007_val)
        create_dataset("VOC2007-test", temp_test_text, temp_folder_images, temp_folder_annotations, folder_voc2007_test)

        # validate dataset
        dataset = Dataset(folder_voc2007_train)
        dataset = Dataset(folder_voc2007_val)
        dataset = Dataset(folder_voc2007_test)

    except Exception:
        print('Failed.')
        shutil.rmtree(folder_voc2007_train)
        shutil.rmtree(folder_voc2007_val)
        shutil.rmtree(folder_voc2007_test)

    finally:
        shutil.rmtree(temp_folder)
    
if __name__ == '__main__':
    main()