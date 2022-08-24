import os
import xml.etree.ElementTree as ET

def convert_pascal_annotations(source, target, overwrite=False):
    assert os.path.exists(source), f"Source {source} don't exists"
    assert overwrite or not os.path.exists(target), f"Target {target} already exists and overwrite is False"
    
    tree = ET.parse(source)
    root = tree.getroot()

    with open(target, "w") as f:

        for child in root:
            if child.tag == 'object':

                class_name = xmin = ymin = xmax = ymax = None
                
                for attribute in child:
                    if attribute.tag == 'name':
                        class_name = attribute.text

                    if attribute.tag == 'bndbox':
                        for cord in attribute:
                            if cord.tag == 'xmin': xmin = int(cord.text)
                            if cord.tag == 'ymin': ymin = int(cord.text)
                            if cord.tag == 'xmax': xmax = int(cord.text)
                            if cord.tag == 'ymax': ymax = int(cord.text)

                assert class_name is not None and xmin is not None and ymin is not None and xmax is not None and ymax is not None, f"Invalid object with class_name {class_name} xmin {xmin} ymin {ymin} xmax {xmax} ymax {ymax}"
                assert xmin <= xmax, f"Invalid object with xmin {xmin} larger than xmax {xmax}"
                assert ymin <= ymax, f"Invalid object with ymin {ymin} larger than ymax {ymax}"

                line = f"{class_name} {xmin} {ymin} {xmax} {ymax}\n"
                f.write(line)

if __name__ == '__main__':

    # converting data/sample/annotations_xml
    convert_pascal_annotations('../data/sample/annotations_xml/000001.xml', '../data/sample/annotations/000001.txt', overwrite=True)
    convert_pascal_annotations('../data/sample/annotations_xml/000002.xml', '../data/sample/annotations/000002.txt', overwrite=True)
    convert_pascal_annotations('../data/sample/annotations_xml/000003.xml', '../data/sample/annotations/000003.txt', overwrite=True)
    convert_pascal_annotations('../data/sample/annotations_xml/000004.xml', '../data/sample/annotations/000004.txt', overwrite=True)
    convert_pascal_annotations('../data/sample/annotations_xml/000005.xml', '../data/sample/annotations/000005.txt', overwrite=True)


