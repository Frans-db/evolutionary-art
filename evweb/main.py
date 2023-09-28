from tap import Tap
from typing import Callable
from torch import Tensor
from html2image import Html2Image

from evolution import *

class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


def evaluate_factory(self, image_path: str) -> Callable[[Tensor], float]:
    def evaluate(image: Tensor) -> float:
        return 0
    return evaluate


def render_page(url: str, filename: str) -> None:
    renderer = Html2Image(output_path='./targets')
    renderer.screenshot(url=url, save_as=filename)

def main():
    experiment = Experiment(
        root='./experiments',
        name='test_experiment',
        population_size=100,
        evaluate=evaluate_factory('./targets/'),
    )
    experiment.run()

if __name__ == '__main__':
    main()