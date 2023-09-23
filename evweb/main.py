from html2image import Html2Image
import argparse
import random

from elements import Element
from evo import Individual, generate_element

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

    element = generate_element(
        p_child=0.5,
        p_class=0.5,
        max_classes=5,
        max_children=5,
        max_depth=2,
        classlist=classlist
    )
    html = data.replace('INNER', element.to_html())
    
    hti = Html2Image(output_path="./experiments")
    hti.screenshot(html_str=html, save_as="out.jpg")
    with open('./experiments/index.html', 'w+') as f:
        f.write(html)


if __name__ == "__main__":
    main()
