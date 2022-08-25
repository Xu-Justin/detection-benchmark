import os
import json
import requests
import datetime
from dataset import Dataset
from utils import strip_ext, create_report

def get_args_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True, help='Path to dataset folder.')
    parser.add_argument('--url', type=str, required=True, help='URL or API endpoint.')
    parser.add_argument('--output', type=str, default='./results', help='Path to store the results.')
    parser.add_argument('--title', type=str, default=None, help='Path to store the results.')
    parser.add_argument('--desc', type=str, default=None, help='Path to store the results.')
    args = parser.parse_args()
    return args

def send_image(url, image_path):

    with open(image_path, "rb") as f:
        image = f.read()

        content_type = 'image/jpeg'
        headers = {'content-type': content_type}
        response = requests.post(url, data=image, headers=headers)
        assert response.status_code == 200, f"Expected response status code of 200, but received {response.status_code}"
        
        response = json.loads(response.text)
    
    return response            

def main(args):
    
    dataset = Dataset(args.dataset)
    
    time = datetime.datetime.now()
    timestamp = f"{time.year}_{time.month}_{time.day}_{time.hour}_{time.minute}_{time.second}"
    
    folder_output = os.path.join(args.output, f"{timestamp}_{dataset.dataset_name}_{args.title}")
    os.makedirs(folder_output)
    
    folder_predictions = os.path.join(folder_output, "predictions")
    os.makedirs(folder_predictions)

    for i in range(dataset.num_of_images):
        image_path = dataset.get_image_path(i)
        response = send_image(args.url, image_path)
        
        predictions = ""
        for bbox in response:
            class_name = str(bbox['class'])
            confidence = float(bbox['confidence'])
            xmin = int(bbox['xmin'])
            ymin = int(bbox['ymin'])
            xmax = int(bbox['xmax'])
            ymax = int(bbox['ymax'])
            prediction = f"{class_name} {confidence} {xmin} {ymin} {xmax} {ymax}\n"
            predictions += prediction

        prediction_file_name = strip_ext(os.path.basename(image_path)) + '.txt'
        prediction_path = os.path.join(folder_predictions, prediction_file_name)

        with open(prediction_path, "w") as f:
            f.write(predictions)

    report_file_name = "report.md"
    report_path = os.path.join(folder_output, report_file_name)
    create_report(dataset, report_path, folder_predictions, args.title, args.desc)
    
if __name__ == '__main__':
    args = get_args_parser()
    print(args)
    main(args)