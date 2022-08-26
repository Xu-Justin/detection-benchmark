from dataset import Dataset
from utils import create_report, print_metrics

def get_args_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True, help='Path to dataset folder.')
    parser.add_argument('--predictions', type=str, required=True, help='Path to predictions.')
    parser.add_argument('--output', type=str, default=None, help='Path to store the report.')
    parser.add_argument('--title', type=str, default=None, help='Path to store the results.')
    parser.add_argument('--desc', type=str, default=None, help='Path to store the results.')
    args = parser.parse_args()
    return args

def main(args):
    
    dataset = Dataset(args.dataset)
    
    folder_predictions = args.predictions

    metrics = dataset.calculate_mAP(folder_predictions)
    print_metrics(metrics)
    
    if args.output is not None:
        create_report(dataset, args.output, metrics, args.title, args.desc)
        print(f"Report saved to {args.output}")
    
if __name__ == '__main__':
    args = get_args_parser()
    print(args)
    main(args)