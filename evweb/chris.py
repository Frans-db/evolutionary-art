from dataclasses import dataclass
import random
import numpy as np
import random
import numpy.typing as npt
from PIL import Image, ImageDraw
import math

number_of_generations = 1000
population_size = 256
number_of_polygons = 256
number_of_vertices = 3
resolution = 128

selection_cutoff = 0.15
mutation_chance = 0.05
mutation_amount = 0.1

gene_size = 4 + number_of_vertices * 2
dna_size = number_of_polygons * gene_size

@dataclass
class Individual:
    mother: "Individual" = None
    father: "Individual" = None
    dna: npt.NDArray = None
    fitness: int = -1

    def __post_init__(self) -> None:
        dna = []
        if self.mother and self.father:
            # Clean up parents
            self.mother.mother = None
            self.mother.father = None
            self.father.mother = None
            self.father.father = None
            # inherit genes
            for i in range(0, dna_size, gene_size):
                parent = self.father if random.random() < 0.5 else self.mother
                for j in range(gene_size):
                    gene = parent.dna[i + j]
                    # mutation
                    if random.random() < mutation_chance:
                        mutation = (
                            random.random() * mutation_amount * 2 - mutation_amount
                        )
                        gene += mutation
                    dna.append(gene)
        else:
            # random individual
            for _ in range(0, dna_size, gene_size):
                dna.extend(
                    [
                        random.random(),  # R
                        random.random(),  # G
                        random.random(),  # B
                        max(random.random() * random.random(), 0.2),  # A
                    ]
                )
                x, y = random.random(), random.random()
                for _ in range(number_of_vertices):
                    dna.extend(
                        [
                            x + random.random() - 0.5,  # X
                            y + random.random() - 0.5,  # Y
                        ]
                    )

        self.dna = np.array(dna).clip(0, 1)
        self.rendered = self.render()

    def render(self) -> npt.NDArray:
        image = Image.new("RGB", (resolution, resolution), color=(0, 0, 0))
        draw = ImageDraw.Draw(image, "RGBA")

        for i in range(0, dna_size, gene_size):
            r = math.floor(self.dna[i + 0] * 255)
            g = math.floor(self.dna[i + 1] * 255)
            b = math.floor(self.dna[i + 2] * 255)
            a = math.floor(self.dna[i + 3] * 255)

            x1 = math.floor(self.dna[i + 4] * resolution)
            y1 = math.floor(self.dna[i + 5] * resolution)
            x2 = math.floor(self.dna[i + 6] * resolution)
            y2 = math.floor(self.dna[i + 7] * resolution)
            x3 = math.floor(self.dna[i + 8] * resolution)
            y3 = math.floor(self.dna[i + 9] * resolution)

            triangles = [(x1, y1), (x2, y2), (x3, y3)]
            draw.polygon(triangles, fill=(r, g, b, a))

        del draw
        return np.asarray(image)

    def evaluate(self, target: npt.NDArray) -> float:
        diff = (target - self.rendered).sum()
        return diff
    
    def get_difference(self, target: npt.NDArray) -> npt.NDArray:
        diff = np.absolute(target - self.rendered).sum(axis=-1) / 3
        return diff


class Population:
    individuals: list[Individual]
    target: npt.NDArray

    def __init__(self, target: npt.NDArray) -> None:
        self.target = target
        self.individuals = []
        for _ in range(population_size):
            individual = Individual()
            individual.fitness = individual.evaluate(target)
            self.individuals.append(individual)

    def iterate(self) -> None:
        if len(self.individuals) < 1:
            return

        size = len(self.individuals)
        offspring = []

        amount_to_select = math.floor(size * selection_cutoff)
        amount_to_generate = math.ceil(1 / selection_cutoff)

        self.individuals.sort(key=lambda x: x.fitness)

        for i in range(amount_to_select):
            for _ in range(amount_to_generate):
                random_individual = i
                while random_individual == i:
                    random_individual = math.floor(random.random() * amount_to_select)
                individual = Individual(
                    mother=self.individuals[i],
                    father=self.individuals[random_individual],
                )
                individual.fitness = individual.evaluate(self.target)
                offspring.append(individual)

        self.individuals = offspring

    def get_fittest(self) -> Individual:
        return min(self.individuals, key=lambda x: x.fitness)
    
    def get_unfittest(self) -> Individual:
        return max(self.individuals, key=lambda x: x.fitness)


def main():
    target = Image.open("./targets/frans.png")
    target = target.resize((resolution, resolution))
    target = np.asarray(target)

    population = Population(target=target)
    for generation in range(number_of_generations):
        population.iterate()

        fittest = population.get_fittest()
        print(f'Generation {generation} - {fittest.fitness}')
        if generation > 0 and generation % 25 == 0:
            image = Image.fromarray(np.uint8(fittest.rendered))
            image.save(f"./experiments/{generation}.png")



if __name__ == "__main__":
    main()



