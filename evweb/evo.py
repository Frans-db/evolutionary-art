from dataclasses import dataclass, field
import random
import copy

from elements import Element


@dataclass()
class Individual:
    element: Element = None
    fitness: float = -1


def generate_element(
    p_child: float,
    p_class: float,
    max_classes: int,
    max_children: int,
    max_depth: int,
    classlist: list[str],
    current_depth: int = 0,
) -> Element:
    classes = []
    for _ in range(max_classes):
        if random.random() < p_class:
            classes.append(random.choice(classlist))
    element = Element("div", classes=classes)

    if current_depth < max_depth:
        for _ in range(max_children):
            if random.random() < p_child:
                child = generate_element(
                    p_child=p_child,
                    p_class=p_class,
                    max_classes=max_classes,
                    max_children=max_children,
                    max_depth=max_depth,
                    classlist=classlist,
                    current_depth=current_depth + 1,
                )
                element.children.append(child)

    return element


def mutate_tag(
    individual: Individual, classlist: list[str], p: float = 0.1
) -> Individual:
    individual = copy.deepcopy(individual)
    if random.random() > p:
        return individual
    elements = individual.element.flatten()
    element = random.choice(elements)

    if random.random() > 0.5:
        child = generate_element(
            p_child=0.5,
            p_class=0.5,
            max_classes=5,
            max_children=1,
            max_depth=2,
            classlist=classlist,
        )
        element.children.append(child)
    elif len(element.children) > 0:
        index = random.randrange(len(element.children))
        element.children.pop(index)

    return individual


def mutate_class(
    individual: Individual, classlist: list[str], p: float = 0.1
) -> Individual:
    individual = copy.deepcopy(individual)
    if random.random() > p:
        return individual
    elements = individual.element.flatten()
    element = random.choice(elements)

    if random.random() > 0.5:
        class_name = random.choice(classlist)
        element.classes.append(class_name)
    elif len(element.children) > 0:
        index = random.randrange(len(element.classes))
        element.classes.pop(index)

    return individual


def crossover(
    individual1: Individual, individual2: Individual
) -> tuple[Individual, Individual]:
    individual1 = copy.deepcopy(individual1)
    individual2 = copy.deepcopy(individual2)

    individual1_elements = individual1.element.flatten()
    individual2_elements = individual2.element.flatten()
    if len(individual1_elements) > 1 and len(individual2_elements) > 1:
        individual1_element = random.choice(individual1_elements[1:])
        individual2_element = random.choice(individual2_elements[1:])

        individual1.element.replace(individual1_element, individual2_element)
        individual2.element.replace(individual2_element, individual1_element)

    return individual1, individual2



def evaluate(individual: Individual) -> float:
    pass
