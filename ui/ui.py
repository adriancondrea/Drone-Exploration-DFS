# imports
from controller.controller import *
from ui.gui import *
from ui.menu.command import *
from ui.menu.console_menu import *


# TODO:create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls

class Ui:
    def __init__(self):
        self._running = True
        self._controller = Controller()
        self._commands = []
        self._commands.append(Command("Exit", "", "", lambda args: True))
        self._commands.append(Command("Configure map", "", "", self.start_map_menu))
        self._commands.append(Command("Configure Evolutionary Algorithm", "", "", self.start_evolutionary_algorithm))

        self._map_menu = ConsoleMenu()
        self._map_menu.register_command(
            Command("create", "create <width> <height> <fill>", "creates a random map", self.create_random_map, True))
        self._map_menu.register_command(Command("load", "load <filename>", "loads a map", self.load_map, True))
        self._map_menu.register_command(Command("save", "save <filename>", "saves a map", self.save_map, True))
        self._map_menu.register_command(Command("view", "view", "displays the map", self.view_map))

        self._ea_menu = ConsoleMenu()
        self._ea_menu.register_command(
            Command("run", "run [count]", "runs the solver [count] or iterations times", self.run_solver, True))
        self._ea_menu.register_command(Command("stats", "stats", "prints the statistics", self.print_statistics))
        self._ea_menu.register_command(
            Command("view", "view", "views the drone moving", self.view_drone_path))

    def start(self, which=0):
        if which == 1:
            self._map_menu.start(True)
            return
        elif which == 2:
            self._ea_menu.start(True)
            return

        while self._running:
            self.print_menu()
            try:
                cmd = int(input(">"))
                if cmd < len(self._commands):
                    res = self._commands[cmd].call(None)
                    if res:
                        return
                else:
                    print("Invalid command")
            except ValueError:
                print("Invalid command")

    def print_menu(self):
        for i in range(len(self._commands)):
            print(str(i) + ". ", self._commands[i].name)

    def start_map_menu(self, _):
        self._map_menu.start(True)
        return False

    def create_random_map(self, args):
        try:
            width = int(args[1])
            height = int(args[2])
            fill = float(args[3])
            self._controller.create_map(width, height, fill)
            self._controller.set_random_drone_location()
        except ValueError:
            print("Invalid command")

    def load_map(self, args):
        self._controller.load_map(args[1])

    def save_map(self, args):
        self._controller.save_map(args[1])

    def view_map(self, args):
        screen = initPyGame(self._controller.get_size())

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            img = image(self._controller.get_map())
            screen.blit(img, (0, 0))
            pygame.display.flip()

        pygame.quit()

    def start_evolutionary_algorithm(self, _):
        self._ea_menu.start(True)
        return True

    def run_solver(self, args):
        if len(args) == 1:
            self._controller.solver()
        else:
            try:
                count = int(args[1])
                self._controller.solver(count)
            except ValueError:
                print("Invalid command")

    def print_statistics(self, args):
        self._controller.statistics()

    def view_drone_path(self, args):
        path = self._controller.get_best_path()
        movingDrone(self._controller.get_map(), self._controller.drone_position, path)
