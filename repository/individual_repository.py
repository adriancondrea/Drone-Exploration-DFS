from model.model import Individual
from numpy import average, nanstd


class IndividualRepository:
    def __init__(self):
        self.population = []
        self.index = 0

    def create_population(self, gene_size, population_size):
        self.population = [Individual(gene_size) for _ in range(population_size)]

    def fitness_average(self):
        return average([individual.get_fitness() for individual in self.population])

    def fitness_standard_deviation(self):
        return nanstd([individual.get_fitness() for individual in self.population])

    def get_fittest_individuals(self, number_of_individuals):
        self.population.sort(reverse=True)
        return self.population[:number_of_individuals]

    def add(self, individual):
        self.population.append(individual)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.population):
            individual = self.population[self.index]
            self.index += 1
            return individual
        else:
            raise StopIteration
