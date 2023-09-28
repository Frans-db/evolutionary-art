from dataclasses import dataclass
from typing import Callable
import os

from .elements import Element, get_default_element
from .images import load_image


@dataclass
class Experiment:
    root: str
    name: str
    population_size: int
    number_of_generations: int

    evaluate: Callable[[Element], float]

    current_generation: int = 0
    experiment_root: str = None
    population: list[Element] = None

    def __post_init__(self) -> None:
        self.experiment_root = os.path.join(self.root, self.name)

    def evaluate_individual(self, individual: Element, index: int) -> None:
        render_dir = os.path.join(self.experiment_root, str(self.current_generation))
        # render individual
        path = individual.render(render_dir, str(index))
        # load rendered image
        image = load_image(path)
        # evaluate image
        individual.fitness = self.evaluate(image)

    def run(self) -> None:
        # create population
        population = [get_default_element() for _ in range(self.population_size)]
        # evaluate population
        for individual_index, individual in enumerate(population):
            self.evaluate_individual(individual, individual_index)
            print(individual.fitness)
        for _ in range(self.number_of_generations):
            self.current_generation += 1
            #   crossover
            #   mutate
            #   evaluate
            #   selection
