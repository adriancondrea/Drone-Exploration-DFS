from time import time

import matplotlib.pyplot

from model.model import *
from repository.individual_repository import IndividualRepository
from repository.run_repository import RunRepository


class Controller:
    def __init__(self):
        self.map = Map()
        self.drone_position = (-1, -1)
        self.battery_capacity = 10
        self.mutation_probability = 0.04
        self.crossover_probability = 0.8
        self.iterations = 30
        self.population_size = 30
        self.number_of_parents = 6
        self.current_run_repository = None
        self.run_repositories = []
        self.set_random_drone_location()

    def iteration(self):
        population = self.current_run_repository.get_last_iteration()
        for individual in population:
            self.compute_fitness(individual)

        # selection of the parents
        fittest_individuals = population.get_fittest_individuals(self.number_of_parents)
        new_generation = IndividualRepository()
        # create offsprings by crossover of the parents
        for _ in range(self.population_size // 2):
            first_parent = choice(fittest_individuals)
            second_parent = choice(fittest_individuals)
            offspring1, offspring2 = first_parent.crossover(second_parent, self.crossover_probability)
            new_generation.add(offspring1)
            new_generation.add(offspring2)
        # apply some mutations
        for individual in new_generation:
            individual.mutate(self.mutation_probability)
        return population, new_generation

    def run(self):
        for i in range(self.iterations):
            population, new_population = self.iteration()
            self.current_run_repository.add_iteration(new_population)

    def solver(self, count=None):
        # TODO:
        # create the population,
        # run the algorithm
        # return the results and the statistics
        if count is None:
            count = 1

        for i in range(count):
            start = time()
            self.current_run_repository = RunRepository(random(), self.battery_capacity, self.population_size)
            self.run_repositories.append(self.current_run_repository)
            self.run()
            end = time()
            print("Duration: ", (end - start) * 1000, " ms for algorithm ", i + 1)

    def compute_fitness(self, individual: Individual):
        fitness = 0
        position = self.drone_position
        n = self.map.getN()
        m = self.map.getM()
        map_surface = np.zeros((m, n))
        map_surface[position[0]][position[1]] = 1
        self.discover_map(position, map_surface)

        for gene in individual.get_genes():
            x, y = position[0] + gene[0], position[1] + gene[1]
            # if drone is out of bounds
            if not self.map.validCoordinates(x, y):
                fitness -= 10
                continue
            # if drone hits a wall
            if self.map.getSurfaceValue(x, y) == 1:
                fitness -= 10
                continue
            # if drone goes to a position already visited
            if map_surface[x][y] == 1:
                fitness -= 8
                continue
            map_surface[x][y] = 1
            position = [x, y]
            self.discover_map(position, map_surface)
        fitness += len([x for x in range(self.map.getM()) for y in range(self.map.getN()) if map_surface[x][y] == 2])
        individual.set_fitness(fitness)

    def discover_map(self, starting_position, map_surface):
        for direction in indexVariations:
            x = starting_position[0] + direction[0]
            y = starting_position[1] + direction[1]
            while self.map.validCoordinates(x, y) and self.map.getSurfaceValue(x, y) != 1:
                if map_surface[x][y] == 0:
                    map_surface[x][y] = 2
                x += direction[0]
                y += direction[1]

    def create_map(self, n, m, fill):
        self.map = Map(n, m)
        self.map.randomMap(fill)

    def save_map(self, filename):
        self.map.save_map(filename)

    def load_map(self, filename):
        self.map.load_map(filename)

    def get_map(self):
        return self.map

    def set_random_drone_location(self):
        while True:
            x = randint(0, self.map.getM() - 1)
            y = randint(0, self.map.getN() - 1)
            if self.map.getSurfaceValue(x, y) == EMPTY:
                self.drone_position = (x, y)
                return

    def set_iterations(self, iterations):
        self.iterations = iterations

    def set_battery_capacity(self, capacity):
        self.battery_capacity = capacity

    def set_population_size(self, population_size):
        self.population_size = population_size

    def statistics(self):
        fitness = []
        i = 1
        print("Run number | Random seed | Fitness")
        for repository in self.run_repositories:
            individual = repository[self.iterations - 1].get_fittest_individuals(1)[0]
            fitness.append(individual.fitness)
            print(i, "|", repository.seed, "|", individual.fitness)
            i += 1
        print("Average fitness:", np.average(fitness), "; Standard deviation:", np.nanstd(fitness))
        x = []
        y = []
        z = []
        for i in range(self.iterations):
            x.append(i)
            population = self.current_run_repository[i]
            y.append(population.get_fittest_individuals(1)[0].get_fitness())
            z.append(population.fitness_average())
        matplotlib.pyplot.plot(x, y)
        matplotlib.pyplot.plot(x, z)
        matplotlib.pyplot.show()

    def get_best_repository(self):
        best_repository = None
        fitness = 0
        for repository in self.run_repositories:
            best_individual = repository[self.iterations - 1].get_fittest_individuals(1)[0]
            if best_individual.get_fitness() > fitness:
                fitness = best_individual.get_fitness()
                best_repository = repository
        return best_repository

    def get_best_path(self):
        repository = self.get_best_repository()
        fittest_individual = repository[self.iterations - 1].get_fittest_individuals(1)[0]
        return [gene.direction for gene in fittest_individual.get_genes()]

    def get_drone_position(self):
        return self.drone_position

    def get_size(self):
        return self.map.getM() * BRICK_M, self.map.getN() * BRICK_N
