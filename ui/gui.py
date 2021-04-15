import time
from copy import deepcopy

import pygame

from constants.constants import *


def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("textures/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with ACO")

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def movingDrone(currentMap, path, speed=1):
    # animation of a drone on a path
    screen = initPyGame((currentMap.m * 20, currentMap.n * 20))

    drona = pygame.image.load("textures/drona.png")

    sensor = pygame.image.load("textures/sensor.png")

    brick = pygame.Surface((20, 20))
    brick.fill(GREEN)

    discovered = pygame.Surface((20, 20))
    discovered.fill(RED)

    for square_index in range(len(path)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        screen.blit(draw_map(currentMap), (0, 0))
        for j in range(square_index + 1):
            screen.blit(brick, (path[j][1] * 20, path[j][0] * 20))

        for square in path[:square_index + 1]:
            if currentMap.getSurfaceValue(square[0], square[1]) == SENSOR:
                i, j = square[0], square[1]
                neighbours = [[i, j]] * 4
                for _ in range(square[2]):
                    for direction in directions:
                        new_neighbour = deepcopy(neighbours[direction])
                        new_neighbour[X] += indexVariations[direction][X]
                        new_neighbour[Y] += indexVariations[direction][Y]
                        if (currentMap.validCoordinates(new_neighbour[X], new_neighbour[Y]) and
                                currentMap.getSurfaceValue(new_neighbour[X], new_neighbour[Y]) != WALL):
                            neighbours[direction] = new_neighbour
                            screen.blit(discovered, (new_neighbour[Y] * 20, new_neighbour[X] * 20))

        for i in range(currentMap.n):
            for j in range(currentMap.m):
                if currentMap.surface[i][j] == SENSOR:
                    screen.blit(sensor, (j * 20, i * 20))
        screen.blit(drona, (path[square_index][Y] * 20, path[square_index][X] * 20))
        pygame.display.flip()
        time.sleep(speed)

    time.sleep(50)
    pygame.quit()


def draw_map(currentMap, colour=BLUE, background=WHITE):
    # creates the image of a map

    imagine = pygame.Surface((currentMap.m * BRICK_M, currentMap.n * BRICK_N))
    brick = pygame.Surface((BRICK_M, BRICK_N))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if currentMap.surface[i][j] == WALL:
                imagine.blit(brick, (j * BRICK_M, i * BRICK_N))

    return imagine
