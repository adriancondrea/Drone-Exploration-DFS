import pickle
from random import randint

from model import *


class Controller:
    def __init__(self, environment=Environment(), drone=Drone()):
        self.__environment = environment
        self.__drone = drone
        self.__drone.setPosition(self.randomPosition())
        self.__destination = self.randomPosition()

    def getEnvironmentMapSurface(self):
        return self.__environment.getSurface()

    def saveEnvironment(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self.__environment, f)
            f.close()

    def loadEnvironment(self, numFile):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.__environment.setN(dummy.__n)
            self.__environment.setM(dummy.__m)
            self.__environment.setSurface(dummy.__surface)
            f.close()

    def getDroneLocation(self):
        return self.__drone.getX(), self.__drone.getY()

    def getDestinationLocation(self):
        return self.__destination

    def mark_path(self, current_node=None):
        current = current_node
        while current is not None:
            self.__environment.setValue(current.getX(), current.getY(), 2)
            current = current.parent

    def astar_search(self, cost=1):
        start_node = Node(None, self.__drone.getCoordinates())
        end_node = Node(None, self.__destination)

        # initialize to_visit_list and visited_list
        to_visit_list = []
        visited_list = []
        to_visit_list.append(start_node)

        current_iterations = 0
        max_iterations = (self.__environment.getN() * self.__environment.getM())

        while to_visit_list:
            current_iterations += 1
            current_node = to_visit_list[0]
            current_index = 0
            for index, item in enumerate(to_visit_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            if current_iterations > max_iterations:
                print("Giving up the search, too many iterations!")
                self.mark_path(current_node)
                return
            to_visit_list.pop(current_index)
            visited_list.append(current_index)
            if current_node == end_node:
                self.mark_path()
                return

            children = []
            for direction in directions:
                childrenX = current_node.position[0] + indexVariations[direction][0]
                childrenY = current_node.position[1] + indexVariations[direction][1]

                if self.__environment.validCoordinates(childrenX, childrenY) \
                        and self.__environment.getSurfaceValue(childrenX, childrenY) == 0:
                    children_node = Node(current_node, (childrenX, childrenY))
                    children.append(children_node)

            for child in children:
                visited = False
                for visited_node in visited_list:
                    if child == visited_node:
                        visited = True
                if visited:
                    continue

                child.g = current_node.g + cost
                child.h = (child.position[0] - end_node.position[0]) ** 2 + \
                          (child.position[1] - end_node.position[1]) ** 2
                child.f = child.g + child.h
                already_in_to_visit = False
                for to_visit_node in to_visit_list:
                    if child == to_visit_node and child.g > to_visit_node.g:
                        already_in_to_visit = True
                if already_in_to_visit:
                    continue
                to_visit_list.append(child)

    def randomPosition(self):
        x = randint(0, 19)
        y = randint(0, 19)
        # we make sure we don't position the drone on a wall
        while self.__environment.getSurfaceValue(x, y) == WALL:
            x = randint(0, 19)
            y = randint(0, 19)
        return x, y

    def getN(self):
        return self.__environment.getN()

    def getM(self):
        return self.__environment.getM()
