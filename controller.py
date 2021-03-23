import pickle
from random import randint

from model import *


def euclidean_distance(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2


def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


'''
returns the path from start to current node in a list
'''


def path(current_node):
    pathList = []
    current = current_node
    while current is not None:
        pathList.insert(0, current.position)
        current = current.parent
    return pathList


class Controller:
    def __init__(self, map=Map(), drone=Drone()):
        self.map = map
        self.__drone = drone
        self.__drone.setPosition(self.randomPosition())
        self.__destination = self.randomPosition()

    def getMapSurface(self):
        return self.map.getSurface()

    def saveMap(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self.map, f)
            f.close()

    def loadMap(self, numFile):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.map.setN(dummy.n)
            self.map.setM(dummy.m)
            self.map.setSurface(dummy)
            f.close()

    def getDroneLocation(self):
        return self.__drone.getX(), self.__drone.getY()

    def getDestinationLocation(self):
        return self.__destination

    '''
    performs a* search from start to end, with given move cost
    returns a list of moves as a list of pairs [x,y]
    '''

    def astar_search(self, cost=1):
        start_node = Node(None, self.__drone.getCoordinates())
        end_node = Node(None, self.__destination)

        # initialize to_visit_list and visited_list
        to_visit_list = []
        visited_list = []
        to_visit_list.append(start_node)

        current_iterations = 0
        max_iterations = (self.map.getN() * self.map.getM())

        # while we have nodes to visit
        while to_visit_list:
            current_iterations += 1
            current_node = to_visit_list[0]
            current_index = 0
            # selecting the lowest cost node from to_visit_list
            for index, item in enumerate(to_visit_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            # if we get to the maximum number of iteration, mark the current path and exit the method with an error
            if current_iterations > max_iterations:
                return ERROR, path(current_node)
            # remove the lowest cost node from to_visit_list and add it to visited list, so it doesn't get visited again
            to_visit_list.pop(current_index)
            visited_list.append(current_node)
            # if we finished searching, mark path and return success
            if current_node == end_node:
                return SUCCESS, path(current_node)
            # generate children of current node from adjacent squares
            children = []
            for direction in directions:
                childrenX = current_node.position[0] + indexVariations[direction][0]
                childrenY = current_node.position[1] + indexVariations[direction][1]

                if self.map.validCoordinates(childrenX, childrenY) \
                        and self.map.getSurfaceValue(childrenX, childrenY) != WALL:
                    children_node = Node(current_node, (childrenX, childrenY))
                    children.append(children_node)
            for child in children:
                # if children already visited, move to next children
                visited = False
                for visited_node in visited_list:
                    if child == visited_node:
                        visited = True
                if visited:
                    continue
                # compute f,g,h values
                # g - cost from start to current node
                # h - heuristic based estimated cost for current Node to end Node
                # f - total cost of current Node. f = g + h
                child.g = current_node.g + cost
                child.h = euclidean_distance(child.position, end_node.position)
                child.f = child.g + child.h
                # if children is already in to_visit_list, but with a lower g cost, move to next children
                already_in_to_visit = False
                for to_visit_node in to_visit_list:
                    if child == to_visit_node and child.g > to_visit_node.g:
                        already_in_to_visit = True
                if already_in_to_visit:
                    continue
                to_visit_list.append(child)
        # if to_visit_list is empty, and we haven't got to destination, means there is no way from start to
        # end,thus we return ERROR
        return ERROR, path(start_node)

    def greedy_search(self):
        start_node = Node(None, self.__drone.getCoordinates())
        end_node = Node(None, self.__destination)

        # initialize to_visit_list and visited_list
        to_visit_list = []
        visited_list = []
        to_visit_list.append(start_node)

        current_iterations = 0
        max_iterations = (self.map.getN() * self.map.getM())

        # while we have nodes to visit
        while to_visit_list:
            current_iterations += 1
            current_node = to_visit_list[0]
            current_index = 0
            # selecting the lowest cost node from to_visit_list
            for index, item in enumerate(to_visit_list):
                if item.h < current_node.h:
                    current_node = item
                    current_index = index
            # if we get to the maximum number of iteration, mark the current path and exit the method with an error
            if current_iterations > max_iterations:
                return ERROR, path(current_node)
            # remove the lowest cost node from to_visit_list and add it to visited list, so it doesn't get visited again
            to_visit_list.pop(current_index)
            visited_list.append(current_node)
            # if we finished searching, mark path and return success
            if current_node == end_node:
                return SUCCESS, path(current_node)
            # generate children of current node from adjacent squares
            children = []
            for direction in directions:
                childrenX = current_node.position[0] + indexVariations[direction][0]
                childrenY = current_node.position[1] + indexVariations[direction][1]

                if self.map.validCoordinates(childrenX, childrenY) \
                        and self.map.getSurfaceValue(childrenX, childrenY) != WALL:
                    children_node = Node(current_node, (childrenX, childrenY))
                    children.append(children_node)
            for child in children:
                # if children already visited, move to next children
                visited = False
                for visited_node in visited_list:
                    if child == visited_node:
                        visited = True
                if visited:
                    continue
                # compute h values
                # h - heuristic based estimated cost for current Node to end Node
                child.h = manhattan_distance(child.position, end_node.position)
                # if children is already in to_visit_list, but with a lower h cost, move to next children
                already_in_to_visit = False
                for to_visit_node in to_visit_list:
                    if child == to_visit_node and child.h > to_visit_node.h:
                        already_in_to_visit = True
                if already_in_to_visit:
                    continue
                to_visit_list.append(child)
        # if to_visit_list is empty, and we haven't got to destination, means there is no way from start to
        # end,thus we return ERROR
        return ERROR, path(start_node)

    def randomPosition(self):
        x = randint(0, 19)
        y = randint(0, 19)
        # we make sure we don't position the drone on a wall
        while self.map.getSurfaceValue(x, y) == WALL:
            x = randint(0, 19)
            y = randint(0, 19)
        return x, y

    def getN(self):
        return self.map.getN()

    def getM(self):
        return self.map.getM()
