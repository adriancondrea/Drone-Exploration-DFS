# Define sleep time between moves
MOVES_SLEEP_TIME = 1 / 30
END_SLEEP_TIME = 10

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

# define the fill for the random map
FILL = 0.2

# define the values for the surface matrix
UNKNOWN = -1
EMPTY = 0
WALL = 1

# define the values for the visited matrix
NOT_VISITED = 0
VISITED = 1

# define brick size
BRICK_N = 20
BRICK_M = 20

# define screen size for pygame window
DISPLAY_WIDTH = BRICK_M * MAP_M
DISPLAY_HEIGHT = BRICK_N * MAP_N

# define the image size
IMAGE_N = DISPLAY_HEIGHT + BRICK_N
IMAGE_M = DISPLAY_WIDTH + BRICK_M