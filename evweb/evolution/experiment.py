from dataclasses import dataclass
from typing import Callable
import os
from PIL import Image
from torchvision.transforms import ToTensor
from torch import Tensor

from .elements import Element, get_default_element


@dataclass
class Experiment:
    root: str
    name: str
    population_size: int

    evaluate: Callable[[Element], float]

    current_generation: int = 0
    experiment_root: str = None
    population: list[Element] = None

    def __post_init__(self) -> None:
        self.experiment_root = os.path.join(self.root, self.name)

    def evaluate_individual(self, individual: Element, index: int) -> None:
        render_dir = os.path.join(self.experiment_root, str(self.current_generation))
        path = individual.render(render_dir, str(index))
        image = Image.open(path)
        image = ToTensor()(image)
        individual.fitness = self.evaluate(image)

    def run(self) -> None:
        population = [get_default_element() for _ in range(self.population_size)]
        for individual_index, individual in enumerate(population):
            self.evaluate_individual(individual, individual_index)

        # create population
        # evaluate population
        # evaluate individual
        #   render individual
        #       individual doesnt know where to store result
        #       experiment does
        #       add render step?
        # compare to target
        # for each generation
        #   crossover
        #   mutate
        #   evaluate
        #   selection
        pass
