from tap import Tap
from typing import Callable
from torch import Tensor
from torch.nn import MSELoss
from html2image import Html2Image
import copy
import random

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
        name='test',
        root='./experiments'
    )


if __name__ == "__main__":
    main()


# 2568732.75