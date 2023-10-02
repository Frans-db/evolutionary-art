from dataclasses import dataclass
from typing import Callable
import operator
import os
import random
from PIL import Image
import numpy as np

from .individual import Individual


@dataclass
class GeneticAlgorithm:
    experiment_name: str
    root: str
    population_size: int
    number_of_generations: int
    comparator: str

    initialise_individual: Callable[[], Individual]
    evaluate: Callable[[Individual], float]
    crossover: Callable[[Individual, Individual], tuple[Individual, Individual]]
    mutate: Callable[[Individual], Individual]

    current_generation: int = 0
    experiment_root: str = None
    population: list[Individual] = None
    best_individual: Individual = None
    # cmp actually takes 2 _SupportsComparison, but we only give it float
    cmp: Callable[[float, float], bool] = None

    def __post_init__(self) -> None:
        self.experiment_root = os.path.join(self.root, self.experiment_name)
        if self.comparator == "<":
            self.cmp = operator.lt
        elif self.comparator == ">":
            self.cmp = operator.gt

    def evaluate_population(self, population: list[Individual]) -> None:
        # TODO: Allow for multithreaded evaluation
        for individual in population:
            individual.fitness = self.evaluate(individual)
            # Replace best individual if this one is better
            if self.cmp(individual.fitness, self.best_individual.fitness):
                self.best_individual = individual

    def create_offspring(self, population: list[Individual]) -> list[Individual]:
        offspring = []
        random.shuffle(population)
        # TODO: Allow for multithreaded crossover
        for i in range(len(population) // 2):
            # Select 2 individuals from the population
            individual_a = population[i]
            individual_b = population[i + 1]
            # Create 2 children using crossover
            child_a, child_b = self.crossover(individual_a, individual_b)
            # Mutate children and add them to the offspring
            offspring.append(self.mutate(child_a))
            offspring.append(self.mutate(child_b))
        return offspring

    def best_selection(self, population: list[Individual]) -> Individual:
        best_individual = population[0]
        for individual in population:
            if self.cmp(individual.fitness, best_individual.fitness):
                best_individual = individual
        return best_individual

    def tournament_selection(self, population: list[Individual]) -> list[Individual]:
        tournament_size = 4
        number_of_rounds = tournament_size // 2
        selection = []
        for _ in range(number_of_rounds):
            random.shuffle(population)
            number_of_tournaments = len(population) // tournament_size
            for i in range(number_of_tournaments):
                tournament = population[tournament_size * i : tournament_size * (i + 1)]
                selected = self.best_selection(tournament)
                selection.append(selected)
        return selection

    def run(self) -> None:
        self.population = []
        # initialise population
        for _ in range(self.population_size):
            self.population.append(self.initialise_individual())
        self.best_individual = self.population[0]
        # evaluate population
        self.evaluate_population(self.population)

        for _ in range(self.number_of_generations):
            print(f"{self.current_generation}: {self.best_individual.fitness}")
            self.current_generation += 1
            # create offspring
            offspring = self.create_offspring(self.population)
            # evaluate offspring
            self.evaluate_population(offspring)
            im = Image.fromarray(np.uint8(self.best_individual.render()))
            im.save(f"./experiments/{self.current_generation}.png")
            # select from population + offspring
            selection = self.tournament_selection(self.population + offspring)
            # set population to selected
            self.population = selection
