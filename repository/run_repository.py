import random
from repository.individual_repository import IndividualRepository


class RunRepository:
    def __init__(self, seed, gene_size, population_size):
        random.seed(seed)
        self.seed = seed
        population = IndividualRepository()
        population.create_population(gene_size, population_size)
        self.populations = [population]
        self.gene_size = gene_size
        self.population_size = population_size

    def get_last_iteration(self):
        return self.populations[-1]

    def add_iteration(self, population):
        self.populations.append(population)

    def __getitem__(self, item):
        return self.populations[item]

    def get_seed(self):
        return self.seed
