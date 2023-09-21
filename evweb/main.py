from html2image import Html2Image
import argparse
from elements import Element

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
    
    element = Element('div', classes=['w-16', 'h-16', 'bg-red-500'])
    child1 = Element('div', classes=['w-8', 'h-8', 'bg-green-500'])
    child2 = Element('div', classes=['w-8', 'h-8', 'ml-8', 'bg-green-500'])
    element.children.append(child1)
    element.children.append(child2)
    html = element.to_html()
    with open('./html/index.html') as f:
        data = f.read()
    data = data.replace('INNER', html)
    hti = Html2Image(output_path='./experiments')
    hti.screenshot(
        html_str=data, save_as='out.jpg'
    )


if __name__ == '__main__':
    main()