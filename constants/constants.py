# Define sleep time between moves

# Creating some colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
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
MAP_SIZE = 20

# define the fill for the random map and for the sensors
WALLS_FILL = 0.2
SENSORS_FILL = 0.1

# define the values for the surface matrix
EMPTY = 0
WALL = 1
SENSOR = 2

MAX_SENSOR_VISIBILITY = 5

# define brick size
BRICK_SIZE = 20

PARAM_ANTS = 100
PARAM_ITERATIONS = 200
PARAM_ALPHA = 1.9
PARAM_BETA = 0.9
PARAM_RHO = 0.05
PARAM_Q0 = 0.5
PARAM_BATTERY = 70
