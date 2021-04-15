from controller.controller import Controller
from model.model import *
from ui.gui import movingDrone


class Command:
    def __init__(self):
        self.map = Map()
        self.map.randomMap()

        self.controller = Controller(Drone(PARAM_BATTERY), self.map)

    def run(self):
        solution = None

        for _ in range(PARAM_ITERATIONS):
            current_solution = self.controller.iterate()
            if not solution or solution.check_coverage() < current_solution.check_coverage():
                solution = current_solution

        print(solution.check_coverage())
        movingDrone(self.map, solution.path)
