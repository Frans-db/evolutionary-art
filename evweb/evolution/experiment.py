from dataclasses import dataclass, field
from typing import Callable
import os

from ..elements import Element, get_default_element


@dataclass
class Experiment:
    root: str
    name: str
    population_size: int
    current_generation: int = 0
    experiment_root: str = None
    population: list[Element] = None

    evaluate: Callable[[Element], float]

    def __post_init__(self) -> None:
        self.experiment_root = os.path.join(self.root, self.name)
        os.makedirs(self.experiment_root, exist_ok=True)

    def run(self) -> None:
        population = [get_default_element() for _ in range(self.population_size)]
        for individual_index, individual in enumerate(population):
            render_dir = os.path.join(self.experiment_root, self.current_generation)
            individual.render(render_dir, str(individual_index))
            individual.fitness = self.evaluate(individual)

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
