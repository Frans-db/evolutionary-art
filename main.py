import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--taglist', type=str)

    return parser.parse_args()

def load_taglist(path: str):
    with open(path) as f:
        data = f.read()

def main():
    args = parse_args()
    with open(args.taglist) as f:
        data = f.read()
    print(data)
    

if __name__ == '__main__':
    main()