class Skill:
	def __init__(self, name: str, level: int = 0, max_level: int = 450):
		self.__name = name
		self.__level = level
		self.__max_level = max_level

	def __str__(self):
		return f'{self.name()} {self.level()}/{self.max_level()}'

	def __repr__(self):
		return self.__str__()

	def name(self) -> str:
		return self.__name

	def level(self) -> int:
		return self.__level

	def max_level(self) -> int:
		return self.__max_level
