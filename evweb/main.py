from html2image import Html2Image
from tap import Tap
import random

from elements import Element
from evo import *

class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


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

def render():
    hti = Html2Image(output_path='./targets/')
    hti.screenshot(url='https://pypi.org/project/html2image/', save_as='target.png')

def main() -> None:
    args = ArgumentParser().parse_args()
    classlist = load_classlist(args.classlist)
    evolution = Evolution(
        p_child=0.5,
        p_class=0.5,
        max_classes=5,
        max_children=3,
        max_depth=3,
        classlist=classlist,
        p_mutate_tag=0.05,
        p_mutate_class=0.05,
        target_path='./targets/target.png'
    )
    algorithm = GeneticAlgorithm(
        root='./experiments/',
        name='test',
        population_size=args.population_size,
        num_generations=args.num_generations,
        evolution=evolution
    )
    algorithm.run()

if __name__ == "__main__":
    main()