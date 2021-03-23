import time

import pygame

from constants import *


def display_with_path(environment_image, path, mark):
    for move in path:
        environment_image.blit(mark, (move[Y] * BRICK_M, move[X] * BRICK_N))
    return environment_image


class View:
    def __init__(self, controller):
        self.__controller = controller

    def environmentImage(self, background=GRAY_BLUE):
        image = pygame.Surface((IMAGE_M, IMAGE_N))
        image.fill(background)

        brick = pygame.image.load("textures/brick.png")
        empty = pygame.image.load("textures/road.png")
        destination = pygame.image.load("textures/destination.png")
        drone = pygame.image.load("textures/drona.png")

        environment = self.__controller.getMapSurface()
        n = self.__controller.getN()
        m = self.__controller.getM()
        xFinal, yFinal = self.__controller.getDestinationLocation()
        xDrone, yDrone = self.__controller.getDroneLocation()

        for i in range(n):
            for j in range(m):
                if environment[i][j] == WALL:
                    image.blit(brick, (j * BRICK_M, i * BRICK_N))
                else:
                    image.blit(empty, (j * BRICK_M, i * BRICK_N))

        image.blit(destination, (yFinal * BRICK_M, xFinal * BRICK_N))
        image.blit(drone, (yDrone * BRICK_M, xDrone * BRICK_N))
        return image

    def run(self):
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("textures/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Pathfinding in a simple environment")
        star = pygame.image.load("textures/star.png")
        greedy = pygame.image.load("textures/greedy.png")

        screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        screen.fill(WHITE)
        # execute A* search
        astar_start_time = time.time()
        execution_result = self.__controller.astar_search()
        astar_end_time = time.time()
        if execution_result[0] == SUCCESS:
            print("A* execution time: %s" % (astar_end_time - astar_start_time))
        else:
            print("Could not complete A* search!")
        # execute Greedy search
        greedy_start_time = time.time()
        greedy_execution_result = self.__controller.greedy_search()
        greedy_end_time = time.time()
        if greedy_execution_result[0] == SUCCESS:
            print("Greedy execution time: %s" % (greedy_end_time - greedy_start_time))
        else:
            print("Could not complete Greedy search!")

        running = True
        while running:
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
            # display A*
            screen.blit(display_with_path(self.environmentImage(), execution_result[1], star), (0, 0))
            pygame.display.flip()
            time.sleep(2)
            # display Greedy
            screen.blit(display_with_path(self.environmentImage(), greedy_execution_result[1], greedy), (0, 0))
            pygame.display.flip()
            time.sleep(2)
