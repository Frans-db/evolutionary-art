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
    num_triangles: int
    canvas_size: int
    genome_length: int
    genome: npt.NDArray


    def __init__(self, number_of_triangles: int, canvas_size: int) -> None:
        self.canvas_size = canvas_size
        self.bits_per_coordinate = int(np.log2(canvas_size))
        # 24 bits for colours and 6 positions
        self.bits_per_triangle = 6*self.bits_per_coordinate * 24
        self.genome_length = self.bits_per_triangle * number_of_triangles
        self.genome = np.random.choice((0, 1), size=self.genome_length)


    def binary2int(self, binary_array):
        return int(binary_array.dot(2**np.arange(binary_array.size)[::-1]))

    def render(self):
        image = Image.new('RGB', (self.canvas_size, self.canvas_size), color=(255, 255, 255))
        draw = ImageDraw.Draw(image, 'RGBA')
        for i in range(self.genome_length // self.bits_per_triangle):
            binary = self.genome[i*self.bits_per_triangle:(i+1)*self.bits_per_triangle]
            r = self.binary2int(binary[0:8])
            g = self.binary2int(binary[8:16])
            b = self.binary2int(binary[16:24])
            coordinate_binary = binary[24:]
            triangles = []
            for j in range(3):
                x = self.binary2int(coordinate_binary[j*self.bits_per_coordinate:(j+1)*self.bits_per_coordinate])
                y = self.binary2int(coordinate_binary[(j+1)*self.bits_per_coordinate:(j+2)*self.bits_per_coordinate])
                triangles.append((x,y))

            draw.polygon(xy=triangles, fill=(r, g, b, 200))

        del draw
        return np.asanyarray(image)


def initialise_factory(number_of_triangles: int, canvas_size: int) -> Callable[[], BinaryIndividual]:
    def initialise_individual() -> BinaryIndividual:
        # Triangle has 3 coordinates (x and y) and 3 colours (r, g, b)
        return BinaryIndividual(number_of_triangles = number_of_triangles, canvas_size = canvas_size)
    return initialise_individual


def evaluate_factory(target) -> Callable[[BinaryIndividual], float]:
    def evaluate(individual: BinaryIndividual) -> float:
        return np.square(target - individual.render()).sum()
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
    mutation_chance = 0.1
    probabilities = (1-mutation_chance, mutation_chance)
    mutation = np.random.choice((0, 1), size=individual.genome_length, p=probabilities)
    individual.genome = (individual.genome + mutation) % 2

    return individual


def main():
    target = Image.open("./targets/monalisa.jpg")
    target = target.resize((64, 64))
    target = np.asarray(target)
    im = Image.fromarray(np.uint8(target))
    im.save("./monalisa.png")

    algorithm = GeneticAlgorithm(
        experiment_name="binary",
        root="./experiments",
        population_size=50,
        number_of_generations=100,
        comparator="<",
        initialise_individual=initialise_factory(number_of_triangles = 125, canvas_size = 64),
        evaluate=evaluate_factory(target),
        crossover=one_point_crossover,
        mutate=mutate,
    )
    algorithm.run()
    im = Image.fromarray(np.uint8(algorithm.best_individual.render()))
    im.save("./best.png")


if __name__ == "__main__":
    main()
