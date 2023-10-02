from tap import Tap

from evolution import GeneticAlgorithm, Individual


class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


# TODO V3:
# - Make everything generic -> use individual
#   - Element can inherit Individual
# - Multiple crossovers (uniform, tree, etc.)
# - Experiment needs to run on any individual
#   - Remove render functionality, this needs to be handled elsewhere
#   - Make population initialization an input function
#   - Add logging to experiment


def main():
    individual = Individual()
    algorithm = GeneticAlgorithm(
        experiment_name="test",
        root="./experiments",
        population_size=50,
        number_of_generations=300,
        initialise_individual=lambda: 0,
        evaluate=lambda x: 0,
        crossover=lambda x, y: 0,
        mutate=lambda x: 0,
        comparator="<",
    )
    print(algorithm)


if __name__ == "__main__":
    main()
