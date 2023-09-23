from dataclasses import dataclass, field
import random

from elements import Element

@dataclass(init=False)
class Individual:
    html: Element
    fitness: float = -1

    def __init__(self) -> None:
        self.html = Element('div')

def generate_element(p_child: float, p_class: float, max_classes: int, max_children: int, max_depth: int, classlist: list[str], current_depth: int = 0) -> Element:
    classes = []
    for _ in range(max_classes):
        if random.random() < p_class:
            classes.append(random.choice(classlist))
    element = Element('div', classes=classes)

    if current_depth < max_depth:
        for _ in range(max_children):
            if random.random() < p_child:
                element.children.append(generate_element(p_child=p_child, p_class=p_class, max_classes=max_classes, max_children=max_children, max_depth=max_depth, classlist=classlist, current_depth=current_depth + 1))

    return element

def mutate_class(individual: Individual, p: float = 0.01) -> Individual:
    if random.random() > p:
        return individual
    elements = individual.html.flatten()


def mutate_tag(individual: Individual, p: float = 0.01) -> Individual:
    if random.random() > p:
        return individual
    elements = individual.html.flatten()
    # add
    element = random.choice(elements)

    # remove
    # select a random element excluding the root
    element = random.choice(elements[1:])


def crossover(individual1: Individual, individual2: Individual) -> tuple[Individual, Individual]:
    pass


def evaluate(individual: Individual) -> float:
    pass
