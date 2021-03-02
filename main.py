from controller import Controller
from view import View

if __name__ == "__main__":
    controller = Controller()
    view = View(controller)
    view.run()
