from time import sleep

import pygame

from constants import *


class View:
    def __init__(self, controller):
        self.__controller = controller

    def discoveredMapImage(self):
        x, y = self.__controller.getDroneLocation()
        image = pygame.Surface((IMAGE_N, IMAGE_M))
        brick = pygame.image.load("textures/brick.png")
        empty = pygame.image.load("textures/road.png")
        unknown = pygame.image.load("textures/unknown.png")

        discoveredMap = self.__controller.getDiscoveredMapSurface()
        rows = self.__controller.getDiscoveredMapRows()
        columns = self.__controller.getDiscoveredMapColumns()
        for i in range(rows):
            for j in range(columns):
                if discoveredMap[i][j] == WALL:
                    image.blit(brick, (j * BRICK_M, i * BRICK_N))
                elif discoveredMap[i][j] == EMPTY:
                    image.blit(empty, (j * BRICK_M, i * BRICK_N))
                else:
                    image.blit(unknown, (j * BRICK_M, i * BRICK_N))
        if x is not None and y is not None:
            drona = pygame.image.load("textures/drona.png")
            image.blit(drona, (y * BRICK_M, x * BRICK_N))
        return image

    def environmentImage(self, colour=BLACK, background=WHITE):
        image = pygame.Surface((IMAGE_N, IMAGE_M))
        brick = pygame.Surface((BRICK_N, BRICK_M))
        brick.fill(colour)
        image.fill(background)
        environment = self.__controller.getEnvironmentMapSurface()
        n = self.__controller.getDiscoveredMapRows()
        m = self.__controller.getDiscoveredMapColumns()
        for i in range(n):
            for j in range(m):
                if environment[i][j] == WALL:
                    image.blit(brick, (j * BRICK_M, i * BRICK_N))
        return image

    def run(self):
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("textures/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")
        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        screen.fill(WHITE)
        # display the environment on the left
        screen.blit(self.environmentImage(), (0, 0))

        # define a variable to control the main loop
        running = True

        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
            self.__controller.markDetectedWalls()
            while self.__controller.notFinished():
                sleep(MOVES_SLEEP_TIME)
                self.__controller.moveDSF()
                self.__controller.markDetectedWalls()
                # display the detected map on the right
                screen.blit(self.discoveredMapImage(), (400, 0))
                pygame.display.flip()
            sleep(END_SLEEP_TIME)
        pygame.quit()
