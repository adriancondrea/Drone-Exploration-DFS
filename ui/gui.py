import time

import pygame

from constants.constants import *


def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("textures/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame():
    # closes the pygame
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    pygame.quit()


def movingDrone(currentMap, drone_position, path, speed=1, markSeen=True):
    # animation of a drone on a path
    screen = initPyGame((currentMap.getM() * 20, currentMap.getN() * 20))

    drona = pygame.image.load("textures/drona.png")

    path = [drone_position] + path
    print(path)

    for i in range(len(path)):
        screen.blit(draw_map(currentMap), (0, 0))
        current_path = [0, 0]
        for j in range(i + 1):
            if markSeen:
                brick = pygame.Surface((20, 20))
                brick.fill(GREEN)
                current_path[0], current_path[1] = (current_path[0] + path[j][0], current_path[1] + path[j][1])
                for direction in indexVariations:
                    x, y = (current_path[0] + direction[0], current_path[1] + direction[1])

                    while 0 <= x < currentMap.getM() and 0 <= y < currentMap.getN() and currentMap.surface[x][y] != 1:
                        screen.blit(brick, (x * 20, y * 20))
                        x += direction[0]
                        y += direction[1]
        screen.blit(drona, (current_path[0] * 20, current_path[1] * 20))
        pygame.display.flip()
        time.sleep(1 * speed)
    closePyGame()


def draw_map(currentMap, colour=BLUE, background=WHITE):
    # creates the image of a map

    imagine = pygame.Surface((currentMap.getM() * 20, currentMap.getN() * 20))
    brick = pygame.Surface((20, 20))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(currentMap.getM()):
        for j in range(currentMap.getN()):
            if currentMap.surface[i][j] == 1:
                imagine.blit(brick, (i * 20, j * 20))

    return imagine
