from tap import Tap
from dataclasses import dataclass
import copy
import random

from evolution import GeneticAlgorithm, Individual


class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


class BinaryIndividual(Individual):
    genome_length: int
    genome: list[int]

    def __init__(self, genome_length: int) -> None:
        self.genome_length = genome_length
        self.genome = [round(random.random()) for _ in range(genome_length)]


def initialise_individual() -> BinaryIndividual:
    return BinaryIndividual(genome_length=100)


def evaluate(individual: BinaryIndividual) -> float:
    return sum(individual.genome)


def uniform_crossover(
    individual_a: BinaryIndividual, individual_b: BinaryIndividual
) -> tuple[BinaryIndividual, BinaryIndividual]:
    individual_a = copy.deepcopy(individual_a)
    individual_b = copy.deepcopy(individual_b)
    for i in range(individual_a.genome_length):
        if random.random() < 0.5:
            continue
        # Swap genes with a 50% chance
        individual_a.genome[i], individual_b.genome[i] = (
            individual_b.genome[i],
            individual_a.genome[i],
        )

    return individual_a, individual_b


def mutate(individual: BinaryIndividual) -> BinaryIndividual:
    individual = copy.deepcopy(individual)
    for i in range(individual.genome_length):
        # 5% chance of flipping a bit
        if random.random() < 0.05:
            new_gene = (individual.genome[i] + 1) % 2
            individual.genome[i] = new_gene
    return individual


def main():
    algorithm = GeneticAlgorithm(
        experiment_name="binary",
        root="./experiments",
        population_size=128,
        number_of_generations=100,
        comparator=">",
        initialise_individual=initialise_individual,
        evaluate=evaluate,
        crossover=uniform_crossover,
        mutate=mutate,
    )
    algorithm.run()


if __name__ == "__main__":
    main()
