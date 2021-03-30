import pickle
from random import *

import numpy as np

from constants.constants import *


class Map:
    def __init__(self, m=MAP_M, n=MAP_N):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.m, self.n))

    def getN(self):
        return self.n

    def getM(self):
        return self.m

    def validCoordinates(self, x, y):
        return 0 <= x < self.m and 0 <= y < self.n

    def getSurfaceValue(self, x, y):
        return self.surface[x][y]

    def randomMap(self, fill=FILL):
        for i in range(self.m):
            for j in range(self.n):
                if random() <= fill:
                    self.surface[i][j] = WALL

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def save_map(self, filename):
        f = open(filename, 'wb')
        pickle.dump(self, f)
        f.close()

    def load_map(self, filename):
        f = open(filename, 'rb')
        data = pickle.load(f)
        self.m = data.m
        self.n = data.n
        self.surface = data.surface
        f.close()


# we will represent a gene as a pair of direction coordinates (x, y)
class Gene:
    def __init__(self):
        self.direction = choice(indexVariations)

    def __str__(self):
        return '(' + str(self.direction[0]) + ', ' + str(self.direction[1]) + ') '

    def __getitem__(self, item):
        return self.direction[item]



# we will represent an individual as a collection of genes, namely a list of directions
class Individual:
    def __init__(self, size=0):
        self.size = size
        self.genes = [Gene() for _ in range(self.size)]
        self.fitness = None

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, value):
        self.fitness = value

    def get_genes(self):
        return self.genes

    def set_genes(self, value):
        self.genes = value

    def mutate(self, mutateProbability=0.04):
        if random() < mutateProbability:
            # choose a gene to be mutated
            gene_index = randint(0, len(self.genes) - 1)
            self.genes[gene_index] = Gene()

    def crossover(self, otherParent, crossoverProbability=0.8):
        offspring1, offspring2 = Individual(self.size), Individual(self.size)
        if random() < crossoverProbability:
            split_gene_index = randint(1, self.size - 2)
            offspring1.genes = self.genes[:split_gene_index] + otherParent.genes[split_gene_index:]
            offspring2.genes = otherParent.genes[:split_gene_index] + self.genes[split_gene_index:]
            return offspring1, offspring2
        return self, otherParent

    def __lt__(self, other):
        return self.get_fitness() < other.get_fitness()

    def __gt__(self, other):
        return self.get_fitness() > other.get_fitness()

    def __str__(self):
        individual = "Individual: " + str(self.get_fitness) + " genes: "
        for gene in self.genes:
            individual += str(gene)
        return individual
