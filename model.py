from random import random

import numpy as np

from constants import *


class Environment:
    def __init__(self):
        self.__n = MAP_N
        self.__m = MAP_M
        self.__surface = np.zeros((self.__n, self.__m))
        self.randomMap(FILL)

    def valid_coordinates(self, x, y):
        return 0 <= x < self.__n and 0 <= y < self.__m

    def getSurface(self):
        return self.__surface

    def getN(self):
        return self.__n

    def getM(self):
        return self.__m

    def setN(self, n):
        self.__n = n

    def setM(self, m):
        self.__m = m

    def setSurface(self, surface):
        self.__surface = surface

    def validCoordinates(self, x, y):
        return 0 <= x < self.__n and 0 <= y < self.__m

    def getSurfaceValue(self, x, y):
        if self.validCoordinates(x, y):
            return self.__surface[x][y]
        return -1

    def randomMap(self, fill=FILL):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill:
                    self.__surface[i][j] = WALL

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string

    def readUDMSensorsDirection(self, x, y, direction):
        reading = 0
        xf = x + indexVariations[direction][X]
        yf = y + indexVariations[direction][Y]
        while self.validCoordinates(xf, yf) and self.__surface[xf][yf] == EMPTY:
            xf += indexVariations[direction][X]
            yf += indexVariations[direction][Y]
            reading += 1
        return reading

    def readUDMSensors(self, x, y):
        readings = [0, 0, 0, 0]
        for direction in directions:
            readings[direction] = self.readUDMSensorsDirection(x, y, direction)
        return readings

    def setValue(self, x, y, value):
        if self.validCoordinates(x, y):
            self.__surface[x][y] = value


class Drone:
    def __init__(self, x=None, y=None):
        self.__x = x
        self.__y = y

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def setPosition(self, position):
        x = position[0]
        y = position[1]
        self.__x = x
        self.__y = y

    def getCoordinates(self):
        return self.__x, self.__y


class Node:
    '''
    Node class for A* pathfinding
    parent - parent of current Node
    position - current Node cooridnates (x,y)
    g - cost from start to current node
    h - heuristic based estimated cost for current Node to end Node
    f - total cost of current Node. f = g + h
    '''

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = self.h = self.f = 0

    def getX(self):
        return self.position[0]

    def getY(self):
        return self.position[1]

    def __eq__(self, other):
        return isinstance(other, Node) and self.position == other.position
