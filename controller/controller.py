from model.model import *


class Controller:
    def __init__(self, drone, env):
        self.drone = drone
        self.map = env

        self.pheromone_matrix = []
        for i in range(self.map.n):
            row = []
            self.pheromone_matrix.append(row)

            for j in range(self.map.m):
                square = []
                row.append(square)

                for direction in directions:
                    neighbour = [i + indexVariations[direction][X], j + indexVariations[direction][Y]]

                    if self.map.validCoordinates(neighbour[X], neighbour[Y]) \
                            and self.map.getSurfaceValue(neighbour[X], neighbour[Y]) != WALL:
                        if self.map.getSurfaceValue(neighbour[X], neighbour[Y]) == SENSOR:
                            square.append([1] * (MAX_SENSOR_VISIBILITY + 1))
                        else:
                            square.append([1, 0, 0, 0, 0, 0])

                    else:
                        square.append([0] * (MAX_SENSOR_VISIBILITY + 1))

        self.initial_pheromone_matrix = deepcopy(self.pheromone_matrix)

    def iterate(self):
        population = []
        for _ in range(PARAM_ANTS):
            population.append(Ant(self.drone, self.map))

        for _ in range(self.drone.battery_capacity):
            for ant in population:
                ant.increase_path(self.pheromone_matrix, PARAM_ALPHA, PARAM_BETA, PARAM_Q0)

        for i in range(self.map.n):
            for j in range(self.map.m):
                for direction in directions:
                    for spent_energy in range(MAX_SENSOR_VISIBILITY + 1):
                        self.compute_pheromone_matrix(i, j, direction, spent_energy)

        best_coverage, best_solution = max([(ant.check_coverage(), ant) for ant in population],
                                           key=lambda pair: pair[0])

        for ant in population:
            ant_coverage = ant.check_coverage()
            for i in range(len(ant.path) - 1):
                x = ant.path[i]
                y = ant.path[i + 1]
                direction_index = 0
                for direction in directions:
                    if (x[0] + indexVariations[direction][X], x[1] + indexVariations[direction][Y]) == (y[0], y[1]):
                        direction_index = direction
                        break
                self.pheromone_matrix[x[0]][x[1]][direction_index][y[2]] += (ant_coverage + 1) / (
                        (best_coverage + 1) * len(ant.path))
        return best_solution

    def compute_pheromone_matrix(self, i, j, direction_index, spent_energy):
        pheromone_matrix_for_params = self.pheromone_matrix[i][j][direction_index][spent_energy]

        self.pheromone_matrix[i][j][direction_index][spent_energy] = (1 - PARAM_RHO) * pheromone_matrix_for_params + \
                                                                     PARAM_RHO * pheromone_matrix_for_params
