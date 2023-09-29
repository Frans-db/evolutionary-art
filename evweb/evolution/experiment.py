from dataclasses import dataclass
from typing import Callable
import os
import random

from .elements import Element, get_default_element
from .images import load_image


@dataclass
class Experiment:
    root: str
    name: str
    population_size: int
    number_of_generations: int

    evaluate: Callable[[Element], float]
    crossover: Callable[[Element, Element], tuple[Element, Element]]
    selection: Callable[[list[Element]], list[Element]]
    mutate: Callable[[Element], Element]

    current_generation: int = 0
    experiment_root: str = None
    population: list[Element] = None
    best_individual: Element = None

    def __post_init__(self) -> None:
        self.experiment_root = os.path.join(self.root, self.name)

    def evaluate_population(self, population: list[Element]) -> None:
        for individual_index, individual in enumerate(population):
            render_dir = os.path.join(
                self.experiment_root, str(self.current_generation)
            )
            # render individual
            path = individual.render(render_dir, str(individual_index))
            # load rendered image
            image = load_image(path)
            # evaluate image
            individual.fitness = self.evaluate(image)
            if (
                not self.best_individual
                or individual.fitness < self.best_individual.fitness
            ):
                self.best_individual = individual

    def create_offspring(self, population: list[Element]) -> list[Element]:
        offspring = []
        # Shuffle population so crossover is done randomly
        random.shuffle(population)
        for i in range(len(population) // 2):
            # Select 2 individuals
            individual_a = population[i]
            individual_b = population[i + 1]
            # Create 2 children using offspring
            child_a, child_b = self.crossover(individual_a, individual_b)
            offspring.append(self.mutate(child_a))
            offspring.append(self.mutate(child_b))
        return offspring

    def run(self) -> None:
        # create population
        self.population = [get_default_element() for _ in range(self.population_size)]
        # evaluate population
        self.evaluate_population(self.population)
        for _ in range(self.number_of_generations):
            print(f'Generation {self.current_generation}: {self.best_individual.fitness}')
            self.current_generation += 1
            # crossover & mutation
            offspring = self.create_offspring(self.population)
            # evaluation
            self.evaluate_population(offspring)
            # selection
            selection = self.selection(self.population + offspring)
            self.population = selection
