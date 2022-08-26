from .convert import convert_pascal_annotations
from .create_report import create_report

def strip_ext(file_name):
    index = file_name.rindex('.')
    return file_name[:index]

def print_metrics(metrics):
    print(f"AP     : {metrics['map']}")
    print(f"AP_50  : {metrics['map_50']}")
    print(f"AP_75  : {metrics['map_75']}")
    print(f"AR_1   : {metrics['mar_1']}")
    print(f"AR_10  : {metrics['mar_10']}")
    print(f"AR_100 : {metrics['mar_100']}")
    