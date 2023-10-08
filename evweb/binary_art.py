from tap import Tap
import copy
from typing import Callable
import numpy as np
import numpy.typing as npt
import random
from PIL import Image, ImageDraw

from evolution import GeneticAlgorithm, Individual


class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


class BinaryIndividual(Individual):
    genome: npt.NDArray
    genome_length: int
    resolution: int


    def __init__(self, number_of_triangles: int, resolution: int) -> None:
        self.genome = []
        self.genome_length = number_of_triangles * 10
        for _ in range(number_of_triangles):
            self.genome.extend([random.random(),random.random(),random.random(),random.random()])
            x,y = random.random(), random.random()
            for _ in range(3):
                self.genome.append(x + random.random() - 0.5)
                self.genome.append(y + random.random() - 0.5)
        self.genome = np.array(self.genome)
        self.resolution = resolution


    def render(self, resolution: int = None):
        if resolution is None:
            resolution = self.resolution
        image = Image.new('RGB', (resolution, resolution), color=(255, 255, 255))
        draw = ImageDraw.Draw(image, 'RGBA')

        for i in range(self.genome_length // 10):
            r = round(255 * self.genome[10*i+0])
            g = round(255 * self.genome[10*i+1])
            b = round(255 * self.genome[10*i+2])
            o = round(255 * self.genome[10*i+3])

            x1 = round(resolution * self.genome[10*i+4])
            y1 = round(resolution * self.genome[10*i+5])
            x2 = round(resolution * self.genome[10*i+6])
            y2 = round(resolution * self.genome[10*i+7])
            x3 = round(resolution * self.genome[10*i+8])
            y3 = round(resolution * self.genome[10*i+9])
            triangles = [(x1,y1),(x2,y2),(x3,y3)]
            draw.polygon(xy=triangles, fill=(r, g, b, o))

        del draw
        return np.asanyarray(image)


def initialise_factory(number_of_triangles: int, resolution: int) -> Callable[[], BinaryIndividual]:
    def initialise_individual() -> BinaryIndividual:
        return BinaryIndividual(number_of_triangles = number_of_triangles, resolution = resolution)
    return initialise_individual


def mse(object1, object2):
    return (object1 - object2).sum()

def evaluate_factory(target) -> Callable[[BinaryIndividual], float]:
    def evaluate(individual: BinaryIndividual) -> float:
        return mse(target, individual.render())
    return evaluate

def uniform_crossover(
    individual_a: BinaryIndividual, individual_b: BinaryIndividual
) -> tuple[BinaryIndividual, BinaryIndividual]:
    individual_a = copy.deepcopy(individual_a)
    individual_b = copy.deepcopy(individual_b)
    choices = np.random.choice((0,1), size=individual_a.genome_length)
    genome_a = np.where(choices, individual_a.genome, individual_b.genome)
    genome_b = np.where(choices, individual_b.genome, individual_a.genome)
    individual_a.genome = genome_a
    individual_b.genome = genome_b

    return individual_a, individual_b

def one_point_crossover(
    individual_a: BinaryIndividual, individual_b: BinaryIndividual
) -> tuple[BinaryIndividual, BinaryIndividual]:
    individual_a = copy.deepcopy(individual_a)
    individual_b = copy.deepcopy(individual_b)
    point = random.randrange(0, individual_a.genome_length)
    genome_a = np.concatenate((individual_a.genome[:point], individual_b.genome[point:]))
    genome_b = np.concatenate((individual_b.genome[:point], individual_a.genome[point:]))

    individual_a.genome = genome_a
    individual_b.genome = genome_b

    return individual_a, individual_b


def mutate(individual: BinaryIndividual) -> BinaryIndividual:
    individual = copy.deepcopy(individual)

    mutated_genes = np.random.choice((0, 1), size=individual.genome_length, p=(0.95, 0.05))
    mutation = (np.random.random(individual.genome_length) - 0.5)

    individual.genome += mutated_genes * mutation
    individual.genome = individual.genome.clip(min=0, max=1)

    return individual


def main():
    target = Image.open("./targets/monalisa.jpg")
    target = target.resize((64, 64))
    target = np.asarray(target)
    # target = np.zeros((64, 64, 3))

    im = Image.fromarray(np.uint8(target))
    im.save("./monalisa.png")

    algorithm = GeneticAlgorithm(
        experiment_name="binary",
        root="./experiments",
        population_size=50,
        number_of_generations=400,
        comparator="<",
        initialise_individual=initialise_factory(number_of_triangles = 125, resolution = 64),
        evaluate=evaluate_factory(target),
        crossover=one_point_crossover,
        mutate=mutate,
    )
    algorithm.run()
    best = algorithm.best_individual.render()
    im = Image.fromarray(np.uint8(best))
    print(mse(best, target))
    im.save("./best.png")


if __name__ == "__main__":
    main()
