from enum import Enum
from uuid import uuid4

class InvalidArenaTeamType(Exception):
	pass

class ArenaTeam:
	class Type(Enum):
		two_vs_two = uuid4()
		three_vs_three = uuid4()
		four_vs_four = uuid4()
		five_vs_five = uuid4()



		@staticmethod
		def parse(s: str):
			if '2v2' in s:
				return ArenaTeam.Type.two_vs_two
			elif '3v3' in s:
				return ArenaTeam.Type.three_vs_three
			elif '4v4' in s:
				return ArenaTeam.Type.four_vs_four
			elif '5v5' in s:
				return ArenaTeam.Type.five_vs_five
			else:
				raise InvalidArenaTeamType('Failed to parse ArenaTeam.Type from string')

	def __init__(self, name: str, rating: int, type: Type = Type.two_vs_two):
		self.__name = name
		self.__rating = rating
		self.__type = type

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return f'{str(self.__type)} team: {self.__name}, {self.__rating} rating'