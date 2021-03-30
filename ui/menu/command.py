class Command:
	def __init__(self, name, usage, info, func, split=False):
		self.name = name
		self.usage = usage
		self.func = func
		self.info = info
		self.split = split

	def call(self, arguments):
		if self.split:
			return self.func(arguments.split(" "))
		else:
			return self.func(arguments)