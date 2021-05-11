from typing import Optional

class Statistic:
	def __init__(self, value: Optional[str] = None, description: Optional[str] = None):
		self.description = description
		self.value = value

	def __str__(self):
		if self.value is None:
			return 'N/A'
		return f'{self.description}: {self.value}'