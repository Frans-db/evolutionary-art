import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--classlist', type=str)

    return parser.parse_args()

def load_classlist(path: str):
    with open(path) as f:
        data = f.read()
    for line in data.split('\n'):
        split_point = line.find('-')
        class_name = line[:split_point]
        values = line[split_point+1:]
        print(class_name, values)

def main():
    args = parse_args()
    tags = load_classlist(args.classlist)
    

if __name__ == '__main__':
    main()