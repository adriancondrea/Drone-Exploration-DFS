import pickle
from random import randint

import pygame
from pygame.locals import *

from model import *


class Controller:
    def __init__(self, environment=Environment(), discoveredMap=DMap(), drone=Drone()):
        self.__environment = environment
        self.__discoveredMap = discoveredMap
        self.__drone = drone
        self.__visited = np.zeros((self.__discoveredMap.getN(), self.__discoveredMap.getM()))
        self.positionDroneRandom()

        # initialize comebackDirections with None representing the starting position with no comeback direction
        self.__comebackDirections = [None]

    def notFinished(self):
        return len(self.__comebackDirections) != 0

    def getDiscoveredMapRows(self):
        return self.__discoveredMap.getN()

    def getDiscoveredMapColumns(self):
        return self.__discoveredMap.getM()

    def getDiscoveredMapSurface(self):
        return self.__discoveredMap.getSurface()

    def getEnvironmentMapSurface(self):
        return self.__environment.getSurface()

    def markDetectedWallsDirection(self, direction, sensorReading):
        xf = self.__drone.getX() + indexVariations[direction][X]
        yf = self.__drone.getY() + indexVariations[direction][Y]
        while sensorReading > 0:
            self.__discoveredMap.setValue(xf, yf, EMPTY)
            sensorReading -= 1
            xf = xf + indexVariations[direction][X]
            yf = yf + indexVariations[direction][Y]
        if self.__discoveredMap.validCoordinates(xf, yf):
            self.__discoveredMap.setValue(xf, yf, WALL)

    def markDetectedWalls(self):
        x = self.__drone.getX()
        y = self.__drone.getY()
        if x is None or y is None:
            return
        sensorReadings = self.__environment.readUDMSensors(x, y)
        for direction in directions:
            self.markDetectedWallsDirection(direction, sensorReadings[direction])

    def toBeVisited(self, x, y):
        return self.__discoveredMap.validCoordinates(x, y) and self.__discoveredMap.getValue(x, y) == EMPTY and \
               self.__visited[x][y] == NOT_VISITED

    def setVisited(self, x, y):
        if self.__discoveredMap.validCoordinates(x, y):
            self.__visited[x][y] = VISITED

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

    def moveDSF(self):
        x = self.__drone.getX()
        y = self.__drone.getY()
        if self.__comebackDirections:
            # UP
            if self.toBeVisited(x - 1, y):
                self.__comebackDirections.append(DOWN)
                self.setVisited(x - 1, y)
                self.__drone.setX(x - 1)
            # LEFT
            elif self.toBeVisited(x, y - 1):
                self.__comebackDirections.append(RIGHT)
                self.setVisited(x, y - 1)
                self.__drone.setY(y - 1)
            # DOWN
            elif self.toBeVisited(x + 1, y):
                self.__comebackDirections.append(UP)
                self.setVisited(x + 1, y)
                self.__drone.setX(x + 1)
            # RIGHT
            elif self.toBeVisited(x, y + 1):
                self.__comebackDirections.append(LEFT)
                self.setVisited(x, y + 1)
                self.__drone.setY(y + 1)
            else:
                comeback = self.__comebackDirections.pop()
                # if we get back to the starting square with nowhere to go, the drone finished and we remove it from map
                if comeback is None:
                    self.__drone.setX(None)
                    self.__drone.setY(None)
                else:
                    # otherwise, we go back one square
                    self.__drone.setX(x + indexVariations[comeback][X])
                    self.__drone.setY(y + indexVariations[comeback][Y])

    def positionDroneRandom(self):
        x = randint(0, 19)
        y = randint(0, 19)
        # we make sure we don't position the drone on a wall
        while self.__environment.getSurfaceValue(x, y) == WALL:
            x = randint(0, 19)
            y = randint(0, 19)
        self.__drone.setX(x)
        self.__drone.setY(y)

    def move(self):
        x = self.__drone.getX()
        y = self.__drone.getY()
        pressed_keys = pygame.key.get_pressed()
        if x > 0:
            if pressed_keys[K_UP] and self.__discoveredMap.getValue(x - 1, y) == EMPTY:
                self.__drone.setX(x - 1)
        if x < 19:
            if pressed_keys[K_DOWN] and self.__discoveredMap.getValue(x + 1, y) == EMPTY:
                self.__drone.setX(x + 1)

        if y > 0:
            if pressed_keys[K_LEFT] and self.__discoveredMap.getValue(x, y - 1) == EMPTY:
                self.__drone.setY(y - 1)
        if y < 19:
            if pressed_keys[K_RIGHT] and self.__discoveredMap.getValue(x, y + 1) == EMPTY:
                self.__drone.setY(y + 1)
