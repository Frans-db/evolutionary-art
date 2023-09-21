from html2image import Html2Image
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--classlist', type=str)

    return parser.parse_args()

def load_classlist(path: str) -> list[str]:
    with open(path) as f:
        data = f.read()

    classes = []
    for line in data.split('\n'):
        split_point = line.rfind('-')
        class_name = line[:split_point]
        values = line[split_point+1:]
        
        # load a sequence of classess
        if values.startswith('['):
            values = values[1:-1]
            for value in values.split(','):
                classes.append(f'{class_name}-{value}')
            continue
        
        # load a single class
        classes.append(f'{class_name}-{values}')
    
    return classes

def main() -> None:
    args = parse_args()
    classes = load_classlist(args.classlist)
    print(classes)
    
    hti = Html2Image()
    hti.screenshot(
        html_file='./html/index.html', save_as='out.jpg'
    )

if __name__ == '__main__':
    main()