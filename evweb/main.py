from html2image import Html2Image
import argparse
import random

from elements import Element
from evo import *

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--classlist", type=str, required=True)

    return parser.parse_args()


def load_classlist(path: str) -> list[str]:
    with open(path) as f:
        data = f.read()

    classes = []
    for line in data.split("\n"):
        split_point = line.rfind("-")
        class_name = line[:split_point]
        values = line[split_point + 1 :]

        # load a sequence of classess
        if values.startswith("["):
            values = values[1:-1]
            for value in values.split(","):
                classes.append(f"{class_name}-{value}")
            continue

        # load a single class
        classes.append(f"{class_name}-{values}")

    return classes


def main() -> None:
    args = parse_args()
    classlist = load_classlist(args.classlist)

    with open("./html/index.html") as f:
        data = f.read()

    individual1 = Individual(element=generate_element(
        p_child=0.5,
        p_class=0.5,
        max_classes=2,
        max_children=2,
        max_depth=2,
        classlist=classlist
    ))
    individual2 = Individual(element=generate_element(
        p_child=0.5,
        p_class=0.5,
        max_classes=2,
        max_children=2,
        max_depth=2,
        classlist=classlist
    ))

    print(individual1.element.size, individual2.element.size)
    print(individual1)
    print(individual2)
    print('--- crossover ---')
    individual1, individual2 = crossover(individual1, individual2)
    print(individual1.element.size, individual2.element.size)
    print(individual1)
    print(individual2)

if __name__ == "__main__":
    main()
