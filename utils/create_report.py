import os
import datetime

def create_report_header(title, desc):
    time = datetime.datetime.now()
    return (
        f"# {title}\n\n"
        f"Created at {time.day}-{time.month}-{time.year}, {time.hour}:{time.minute}:{time.second}\n\n"
        f"{desc}\n\n"
    )

def create_table(header, contents):
    width = []
    for x in header: width.append(len(x))
    for content in contents:
        for i, x in enumerate(content):
            width[i] = max(width[i], len(x))

    def create_table_row(row):
        markdown = "|"
        for i, x in enumerate(row): markdown += f" {x:{width[i]}} |"
        markdown += "\n"
        return markdown
    
    markdown = ""
    markdown += create_table_row(header)

    markdown += "|"
    for i, _ in enumerate(header): markdown += "-"*(width[i]+2) + "|"
    markdown += "\n"

    for content in contents:
        markdown += create_table_row(content)
    
    return markdown

def create_report_dataset(dataset):
    MAX_REPR_INDEX = 20

    table_header = ["", ""]
    table_contents = [
        ["Dataset Name", f"{dataset.dataset_name}"],
        ["Number of classes", f"{dataset.num_of_classes}"],
        ["Classes", f"{dataset.classes}"],
        ["Number of images", f"{dataset.num_of_images}"],
        ["Images", f"{dataset.images[:min(len(dataset.images), MAX_REPR_INDEX)]}{'(truncated)' if len(dataset.images) > MAX_REPR_INDEX else ''}"]
    ]

    return (
        f"## Dataset\n\n"
        f"{create_table(table_header, table_contents)}\n"
    )

def create_report_metrics(metrics):
    table_header = ["Metric", "Value"]
    table_contents = [
        ["AP", f"{metrics['map']}"],
        ["AP_50", f"{metrics['map_50']}"],
        ["AP_75", f"{metrics['map_75']}"],
        ["AR_1", f"{metrics['mar_1']}"],
        ["AR_10", f"{metrics['mar_10']}"],
        ["AR_100", f"{metrics['mar_100']}"]
    ]

    return (
        f"## Results\n\n"
        f"{create_table(table_header, table_contents)}\n"
    )

def create_report(dataset, output, folder_predictions, title, desc, overwrite=False):
    assert overwrite or not os.path.exists(output), f"Output {output} already exists and overwrite is False"
    
    metrics = dataset.calculate_mAP(folder_predictions)

    markdown = ""
    markdown += create_report_header(title, desc)
    markdown += create_report_dataset(dataset)
    markdown += create_report_metrics(metrics)

    with open(output, "w") as f:
        f.write(markdown)