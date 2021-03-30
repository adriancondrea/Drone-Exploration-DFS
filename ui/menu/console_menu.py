from ui.menu.command import Command


class ConsoleMenu:
    def __init__(self):
        self._running = True
        self._commands = []
        self._commands.append(Command("help", "help", "prints this menu", self.print_commands))
        self._commands.append(Command("exit", "exit", "exists this menu", lambda args: True))

    def start(self, starting_message=False):
        if starting_message:
            print("For help write 'help'")
        while self._running:
            cmd = input(">")
            for command in self._commands:
                if cmd.lower().startswith(command.name):
                    res = command.call(cmd)
                    if res:
                        return

    def print_commands(self, _):
        for command in self._commands:
            print(command.usage, "-", command.info)
        return False

    def register_command(self, command: Command):
        self._commands.append(command)
