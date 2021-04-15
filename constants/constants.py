# Define sleep time between moves
from random import random

# Creating some colors
BLUE = (0, 0, 255)
GRAY_BLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3


# define indexes variations and their associated directions
indexVariations = [[-1, 0], [0, -1], [1, 0], [0, 1]]

directions = [UP, LEFT, DOWN, RIGHT]

# define X and Y axis coordinates in indexVariations
X = 0
Y = 1

# define the dimensions for the map surface
MAP_N = 20
MAP_M = 20

# define the fill for the random map and for the sensors
WALLS_FILL = 0.2
SENSORS_FILL = 0.1

# define the values for the surface matrix
UNKNOWN = -1
EMPTY = 0
WALL = 1
SENSOR = 2

MAX_SENSOR_VISIBILITY = 5

# define brick size
BRICK_N = 20
BRICK_M = 20

# define screen size for pygame window
DISPLAY_WIDTH = BRICK_M * MAP_M
DISPLAY_HEIGHT = BRICK_N * MAP_N

# define the image size
IMAGE_N = DISPLAY_HEIGHT + BRICK_N
IMAGE_M = DISPLAY_WIDTH + BRICK_M

PARAM_ANTS = 100
PARAM_ITERATIONS = 100
PARAM_ALPHA = 1.9
PARAM_BETA = 0.9
PARAM_RHO = 0.05
PARAM_Q0 = 0.5
PARAM_BATTERY = 50


def selection_probabilities(my_list, probabilities):
    while True:
        for i in range(len(my_list)):
            if random() <= probabilities[i]:
                return my_list[i]
