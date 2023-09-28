from tap import Tap
from typing import Callable
from torch import Tensor
from torch.nn import MSELoss
from html2image import Html2Image

from evolution import *


class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


def evaluate_factory(image_path: str) -> Callable[[Tensor], float]:
    loss = MSELoss(reduction="sum")
    target_image = load_image(image_path)

    def evaluate(image: Tensor) -> float:
        return loss(image, target_image).item()

    return evaluate


def render_page(url: str, filename: str) -> None:
    renderer = Html2Image(output_path="./targets")
    renderer.screenshot(url=url, save_as=filename)


def main():
    experiment = Experiment(
        root="./experiments",
        name="test_experiment",
        population_size=10,
        number_of_generations=10,
        evaluate=evaluate_factory("./targets/html2image.png"),
    )
    experiment.run()


if __name__ == "__main__":
    main()
