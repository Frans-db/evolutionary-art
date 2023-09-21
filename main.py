import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--classlist', type=str)

    return parser.parse_args()

def load_classlist(path: str):
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

def main():
    args = parse_args()
    classes = load_classlist(args.classlist)
    print(classes)
    

if __name__ == '__main__':
    main()