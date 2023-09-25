from dataclasses import dataclass, field
from collections.abc import Callable
import random
import copy
import os
from PIL import Image
from torch.nn import MSELoss
from torchvision.transforms import ToTensor


from evweb.elements import Element


@dataclass
class Individual:
    element: Element = None
    fitness: float = -1
    image_path: str = None

    def render(self, directory: str, filename: str):
        self.element.render(directory, filename)
        self.image_path = os.path.join(directory, f'{filename}.png')


@dataclass
class Evolution:
    p_child: float
    p_class: float
    max_classes: int
    max_children: int
    max_depth: int
    classlist: list[str]
    p_mutate_tag: float
    p_mutate_class: float
    target_path: str

    target = None

    def _load_image(self, path: str) -> None:
        image = Image.open(path)
        return ToTensor()(image)

    def __post_init__(self):
        self.target = self._load_image(self.target_path)

    def generate_element(self, current_depth: int = 0):
        classes = []
        for _ in range(self.max_classes):
            if random.random() < self.p_class:
                classes.append(random.choice(self.classlist))
        element = Element("div", classes=classes)

        if current_depth > self.max_depth:
            return element

        next_depth = current_depth + 1
        for _ in range(self.max_children):
            if random.random() > self.p_child:
                continue
            child = self.generate_element(current_depth=next_depth)
            element.children.append(child)

        return element

    def mutate(self, individual: Individual) -> Individual:
        return self.mutate_class(self.mutate_tag(individual))

    def mutate_tag(self, individual: Individual) -> Individual:
        individual = copy.deepcopy(individual)
        if random.random() > self.p_mutate_tag:
            return individual
        elements = individual.element.flatten()
        element = random.choice(elements)

        if random.random() > 0.5:
            child = self.generate_element()
            element.children.append(child)
        elif len(element.children) > 0:
            index = random.randrange(len(element.children))
            element.children.pop(index)

        return individual

    def mutate_class(self, individual: Individual) -> Individual:
        individual = copy.deepcopy(individual)
        if random.random() > self.p_mutate_tag:
            return individual
        elements = individual.element.flatten()
        element = random.choice(elements)

        if random.random() > 0.5:
            class_name = random.choice(self.classlist)
            element.classes.append(class_name)
        elif len(element.classes) > 0:
            index = random.randrange(len(element.classes))
            element.classes.pop(index)

        return individual

    def crossover(
        self, individual1: Individual, individual2: Individual
    ) -> tuple[Individual, Individual]:
        individual1 = copy.deepcopy(individual1)
        individual2 = copy.deepcopy(individual2)

        individual1_elements = individual1.element.flatten()
        individual2_elements = individual2.element.flatten()
        if len(individual1_elements) > 1 and len(individual2_elements) > 1:
            individual1_element = random.choice(individual1_elements[1:])
            individual2_element = random.choice(individual2_elements[1:])

            individual1.element.replace(individual1_element, individual2_element)
            individual2.element.replace(individual2_element, individual1_element)

        return individual1, individual2

    def best_selection(self, population: list[Individual]) -> Individual:
        best_individual: Individual = population[0]
        for individual in population:
            if individual.fitness < best_individual.fitness:
                best_individual = individual
        return individual

    def tournament_selection(self, population: list[Individual]) -> list[Individual]:
        tournament_size = 4
        number_of_rounds = tournament_size // 2
        selection = []
        for _ in range(number_of_rounds):
            random.shuffle(population)
            number_of_tournaments = len(population) // tournament_size
            for i in range(number_of_tournaments):
                tournament = population[tournament_size * i : tournament_size * (i + 1)]
                selected = self.best_selection(tournament)
                selection.append(selected)
        return selection

    def evaluate(self, individual: Individual) -> float:
        image = self._load_image(individual.image_path)
        loss = MSELoss(reduction='sum')(image, self.target)
        return loss.item()


@dataclass
class GeneticAlgorithm:
    root: str
    name: str
    population_size: int
    num_generations: int

    evolution: Evolution

    current_generation: int = 0
    population: list[Individual] = None
    best_individual: Individual = None

    def crossover(self, population: list[Individual]) -> list[Individual]:
        offspring = []
        random.shuffle(population)
        for i in range(len(population) // 2):
            individual1 = population[i]
            individual2 = population[i + 1]
            child1, child2 = self.evolution.crossover(individual1, individual2)
            child1 = self.evolution.mutate(child1)
            child2 = self.evolution.mutate(child2)
            offspring.append(child1)
            offspring.append(child2)
        return offspring

    def run(self):
        self.population = []
        for _ in range(self.population_size):
            element = self.evolution.generate_element()
            self.population.append(Individual(element=element))
        self.evaluate_population(self.population)

        for _ in range(self.num_generations):
            print(self.current_generation, self.best_individual.fitness, self.best_individual.element.size)
            self.current_generation += 1
            offspring = self.crossover(self.population)
            offspring = [self.evolution.mutate(individual) for individual in offspring]
            self.evaluate_population(offspring)
            selection = self.evolution.tournament_selection(self.population + offspring)
            self.population = selection

    def evaluate_population(self, population: list[Individual]):
        for i,individual in enumerate(population):
            filename = f'{i}'
            directory = os.path.join(self.root, self.name, str(self.current_generation))
            individual.render(directory, filename)
            individual.fitness = self.evolution.evaluate(individual)
            if (
                self.best_individual is None
                or individual.fitness < self.best_individual.fitness
            ):
                self.best_individual = individual
