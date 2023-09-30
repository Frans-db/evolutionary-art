from tap import Tap
from dataclasses import dataclass
import copy
import random
import numpy as np
from PIL import Image
from typing import Callable

from evolution import GeneticAlgorithm, Individual


class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int

@dataclass
class Square:
    x: float
    y: float
    width: float
    height: float
    r: float
    g: float
    b: float

class Art(Individual):
    num_squares: int
    size: int
    squares: list[Square]

    def __init__(self, num_squares: int, size: int) -> None:
        self.num_squares = num_squares
        self.size = size
        self.squares = []
        for _ in range(num_squares):
            self.squares.append(Square(
                x=random.random() * size,
                y=random.random() * size,
                width=random.random() * size * 0.2,
                height=random.random() * size * 0.2,
                r=random.random()*255,
                g=random.random()*255,
                b=random.random()*255,
            ))

    def render(self):
        result = np.zeros((self.size, self.size, 3))
        for square in self.squares:
            x_max = int(min(self.size, square.x + square.width))
            y_max = int(min(self.size, square.y + square.height))
            rgb = np.array([square.r, square.g, square.b]).clip(min=0, max=255)
            result[int(square.x):x_max, int(square.y):y_max, :] = rgb
        return result


def initialise_individual() -> Art:
    return Art(num_squares=512,size=256)


def evaluate_factory(target) -> Callable[[Art], float]:
    def evaluate(individual: Art) -> float:
        return np.square(target - individual.render()).sum()
    return evaluate


def crossover(
    individual_a: Art, individual_b: Art
) -> tuple[Art, Art]:
    individual_a = copy.deepcopy(individual_a)
    individual_b = copy.deepcopy(individual_b)

    point = random.randrange(0, individual_a.num_squares)
    squares_a = individual_a.squares[:point] + individual_b.squares[point:]
    squares_b = individual_b.squares[:point] + individual_a.squares[point:]
    individual_a.squares = squares_a
    individual_b.squares = squares_b

    return individual_a, individual_b

def nudge(value: float, min_value: float, max_value: float, percentage: float) -> float:
    nudge = (random.random() - 0.5) * percentage
    value = value + value * nudge
    return max(min(value, max_value), min_value)

def mutate(individual: Art) -> Art:
    individual = copy.deepcopy(individual)
    for square in individual.squares:
        if random.random() < 0.05:
            square.r += (random.random() - 0.5) * 10
            square.g += (random.random() - 0.5) * 10
            square.b += (random.random() - 0.5) * 10
        if random.random() < 0.05:
            square.width += (random.random() - 0.5) * 10
            square.height += (random.random() - 0.5) * 10
        if random.random() < 0.05:
            square.x += (random.random() - 0.5) * 10
            square.y += (random.random() - 0.5) * 10 
    return individual


def main():
    target = Image.open('./targets/monalisa.jpg')
    target = target.resize((256, 256))
    target = np.asarray(target)
    im = Image.fromarray(np.uint8(target))
    im.save('./monalisa.png')

    algorithm = GeneticAlgorithm(
        experiment_name="art",
        root="./experiments",
        population_size=512,
        number_of_generations=256,
        comparator="<",
        initialise_individual=initialise_individual,
        evaluate=evaluate_factory(target=target),
        crossover=crossover,
        mutate=mutate,
    )
    algorithm.run()
    im = Image.fromarray(np.uint8(algorithm.best_individual.render()))
    im.save('./best.png')


if __name__ == "__main__":
    main()
