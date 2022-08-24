from .convert import convert_pascal_annotations
from .create_report import create_report

def strip_ext(file_name):
    index = file_name.rindex('.')
    return file_name[:index]
