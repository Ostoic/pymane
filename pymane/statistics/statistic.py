class Statistic:
	def __init__(self, value: str, description: str):
		self.description = description
		self.value = value

	def __str__(self):
		return f'{self.description}: {self.value}'