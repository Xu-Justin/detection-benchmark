import os
import xml.etree.ElementTree as ET

pascal_classes = [
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

def convert_pascal_annotations(source, target, overwrite=False):
    assert os.path.exists(source), f"Source {source} don't exists"
    assert overwrite or not os.path.exists(target), f"Target {target} already exists and overwrite is False"
    
    tree = ET.parse(source)
    root = tree.getroot()

    with open(target, "w") as f:

        for child in root:
            if child.tag == 'object':
                
                for attribute in child:
                    if attribute.tag == 'name':
                        class_name = attribute.text
                        class_id = pascal_classes.index(class_name)

                    if attribute.tag == 'bndbox':
                        for cord in attribute:
                            if cord.tag == 'xmin': xmin = cord.text
                            if cord.tag == 'ymin': ymin = cord.text
                            if cord.tag == 'xmax': xmax = cord.text
                            if cord.tag == 'ymax': ymax = cord.text

                assert class_id is None or xmin is None or ymin is None or xmax is None or ymax is None, f"Invalid object with class_id {class_id} xmin {xmin} ymin {ymin} xmax {xmax} ymax {ymax}"
                assert xmin <= xmax, f"Invalid object with xmin {xmin} larger than xmax {xmax}"
                assert ymin <= ymax, f"Invalid object with ymin {ymin} larger than ymax {ymax}"

                line = f"{class_id} {xmin} {ymin} {xmax} {ymax}\n"
                f.write(line)

if __name__ == '__main__':

    # converting data/sample/annotations_xml
    convert_pascal_annotations('../data/sample/annotations_xml/000001.xml', '../data/sample/annotations/000001.txt', overwrite=True)
    convert_pascal_annotations('../data/sample/annotations_xml/000002.xml', '../data/sample/annotations/000002.txt', overwrite=True)
    convert_pascal_annotations('../data/sample/annotations_xml/000003.xml', '../data/sample/annotations/000003.txt', overwrite=True)
    convert_pascal_annotations('../data/sample/annotations_xml/000004.xml', '../data/sample/annotations/000004.txt', overwrite=True)
    convert_pascal_annotations('../data/sample/annotations_xml/000005.xml', '../data/sample/annotations/000005.txt', overwrite=True)


