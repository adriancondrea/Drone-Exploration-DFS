from copy import deepcopy
from random import *

import numpy as np

from constants.constants import *


class Map:
    def __init__(self, m=MAP_M, n=MAP_N):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.m, self.n))
        self.visited = None

    def validCoordinates(self, x, y):
        return 0 <= x < self.m and 0 <= y < self.n

    def getSurfaceValue(self, x, y):
        return self.surface[x][y]

    def randomMap(self, walls_fill=WALLS_FILL, sensors_fill=SENSORS_FILL):
        for i in range(self.m):
            for j in range(self.n):
                if random() <= walls_fill:
                    self.surface[i][j] = WALL
                elif random() <= sensors_fill:
                    self.surface[i][j] = SENSOR

    def update_visited(self):
        self.visited = []
        for i in range(self.n):
            visited_row = []
            self.visited.append(visited_row)
            for j in range(self.m):
                readings = [0] * (MAX_SENSOR_VISIBILITY + 1)
                visited_row.append(readings)
                if self.surface[i][j] != SENSOR:
                    continue

                neighbours = [[i, j]] * 4
                squares = 0
                for k in range(1, MAX_SENSOR_VISIBILITY + 1):
                    for direction in directions:
                        new_neighbour = deepcopy(neighbours[direction])
                        new_neighbour[X] += indexVariations[direction][X]
                        new_neighbour[Y] += indexVariations[direction][Y]
                        if self.validCoordinates(new_neighbour[X], new_neighbour[Y]) and self.getSurfaceValue(
                                new_neighbour[X], new_neighbour[Y]) != WALL:
                            squares += 1
                            neighbours[direction] = new_neighbour

                    readings[k] = squares


class Drone:
    def __init__(self, battery_capacity, x=None, y=None):
        if x is None:
            x = randrange(MAP_M)
        if y is None:
            y = randrange(MAP_N)
        self.x = x
        self.y = y
        self.battery_capacity = battery_capacity

    def get_coordinates(self):
        return self.x, self.y


class Ant:
    def __init__(self, drone, env):
        if env.getSurfaceValue(drone.x, drone.y) == SENSOR:
            sensor_energy = min(drone.battery_capacity, randint(0, MAX_SENSOR_VISIBILITY))
        else:
            sensor_energy = 0

        self.path = [(drone.x, drone.y, sensor_energy)]
        self.map = env
        self.spent_energy = np.zeros((env.m, env.n))
        self.spent_energy[drone.x][drone.y] = sensor_energy
        self.battery_left = drone.battery_capacity - sensor_energy

    def check_coverage(self):
        marked = np.full((self.map.m, self.map.n), False)
        for i, j, energy in self.path:
            if not energy:
                continue
            neighbours = [[i, j]] * 4
            for _ in range(energy):
                for direction in directions:
                    new_neighbour = deepcopy(neighbours[direction])
                    new_neighbour[X] += indexVariations[direction][X]
                    new_neighbour[Y] += indexVariations[direction][Y]

                    if self.map.validCoordinates(new_neighbour[X], new_neighbour[Y]) and self.map.getSurfaceValue(
                            new_neighbour[X], new_neighbour[Y]) != WALL:
                        marked[new_neighbour[0]][new_neighbour[1]] = True
                        neighbours[direction] = new_neighbour

        count = 0
        for i in range(self.map.n):
            for j in range(self.map.m):
                if marked[i][j]:
                    count += 1
        return count

    def increase_path(self, pheromone_matrix, alpha, beta, q0):
        current_square = (self.path[-1][0], self.path[-1][1])
        possible_next_squares = []

        for direction in directions:
            for spent_energy in range(min(MAX_SENSOR_VISIBILITY + 1, self.battery_left)):
                tau = pheromone_matrix[current_square[0]][current_square[1]][direction][spent_energy]

                if tau == 0:
                    continue

                cost = (1 / (spent_energy + 1)) ** beta + tau ** alpha
                sight = current_square[X] + indexVariations[direction][X], current_square[Y] + indexVariations[direction][Y], spent_energy
                next_square = [sight, cost]

                if self.spent_energy[sight[0]][sight[1]] <= spent_energy:
                    possible_next_squares.append(next_square)
        if not possible_next_squares:
            return

        if random() < q0:
            next_square = max(possible_next_squares, key=lambda x: x[1])[0]  # max by cost

        else:
            probabilities_sum = sum([move[1] for move in possible_next_squares])
            probabilities = [move[1] / probabilities_sum for move in possible_next_squares]

            next_square = selection_probabilities(possible_next_squares, probabilities)[0]

        spent_energy = next_square[2]

        self.path.append(next_square)
        self.battery_left -= spent_energy + 1
        self.spent_energy[next_square[0]][next_square[1]] = spent_energy
