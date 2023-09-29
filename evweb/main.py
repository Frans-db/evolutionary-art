from tap import Tap
from typing import Callable
from torch import Tensor
from torch.nn import MSELoss
from html2image import Html2Image
import copy
import random

from evolution import *


class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


def evaluate_factory(image_path: str) -> Callable[[Tensor], float]:
    loss = MSELoss(reduction="sum")
    target_image = load_image(image_path)

    def evaluate(image: Tensor) -> float:
        return loss(image, target_image).item()

    return evaluate


def crossover(individual_a: Element, individual_b: Element) -> tuple[Element, Element]:
    individual_a = copy.deepcopy(individual_a)
    individual_b = copy.deepcopy(individual_b)
    elements_a = individual_a.flatten()
    elements_b = individual_b.flatten()
    # Individual only has a root element. This cannot be swapped
    if len(elements_a) < 1 or len(elements_b) < 1:
        return individual_a, individual_b
    # Select a random element from both individuals
    element_a = random.choice(elements_a[1:])
    element_b = random.choice(elements_b[1:])
    # Swap elements
    individual_a.replace(element_a, element_b)
    individual_b.replace(element_b, element_a)

    return individual_a, individual_b


# Select the best individual from a population
def best_selection(population: list[Element]) -> Element:
    best_individual = population[0]
    for individual in population:
        if individual.fitness < best_individual.fitness:
            best_individual = individual
    return best_individual


def tournament_selection(population: list[Element]) -> list[Element]:
    tournament_size = 4
    number_of_rounds = tournament_size // 2
    selection = []
    for _ in range(number_of_rounds):
        random.shuffle(population)
        number_of_tournaments = len(population) // tournament_size
        for i in range(number_of_tournaments):
            tournament = population[tournament_size * i : tournament_size * (i + 1)]
            selected = best_selection(tournament)
            selection.append(selected)
    return selection


def mutate(individual: Element) -> Element:
    individual = copy.deepcopy(individual)
    for property in individual.properties:
        if random.random() < 0.05:
            property.mutate()
    return individual

def render_page(url: str, filename: str) -> None:
    renderer = Html2Image(output_path="./targets")
    renderer.screenshot(url=url, save_as=filename)


def main():
    experiment = Experiment(
        root="./experiments",
        name="test_experiment",
        population_size=200,
        number_of_generations=100,
        evaluate=evaluate_factory("./targets/html2image.png"),
        crossover=crossover,
        selection=tournament_selection,
        mutate=mutate
    )
    experiment.run()


if __name__ == "__main__":
    main()


# 2568732.75