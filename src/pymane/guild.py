from pymane.log import get_logger

log = get_logger(__name__)

class Guild:
	def __init__(self, name: str):
		self.__name = name

	def name(self) -> str:
		return self.__name