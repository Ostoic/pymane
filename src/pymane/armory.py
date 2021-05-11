from .log import get_logger
from .character import Character

log = get_logger(__name__)

class Armory:
	def __init__(self, session):
		self.session = session

	def character(self, name: str, realm: str = 'Icecrown') -> Character:
		return Character(name=name, realm_name=realm, armory=self)


