from tap import Tap

from evolution import *

class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


def main():
    experiment = Experiment(
        root='./experiments',
        name='test_experiment',
        population_size=100
    )
    print(experiment)

if __name__ == '__main__':
    main()