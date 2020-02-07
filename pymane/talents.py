from typing import List

class TalentSpec:
	def __init__(self, name: str, tree1_points: int = 0, tree2_points: int = 0, tree3_points: int = 0):
		self.__name = name
		self.__tree_points = [tree1_points, tree2_points, tree3_points]

	def __str__(self):
		return f'{self.name()} {self.tree_points()[0]}/{self.tree_points()[1]}/{self.tree_points()[2]}'

	def __repr__(self):
		return self.__str__()

	def name(self) -> str:
		return self.__name

	def tree_points(self) -> List[int]:
		return self.__tree_points


