from pymane.log import get_logger

log = get_logger(__name__)

class Race:
	def __init__(self, name: str):
		self.name = name

	def __str__(self):
		return self.name

# Alliance
gnome = Race('Gnome')
night_elf = Race('Night Elf')
human = Race('Human')
draenei = Race('Draenei')
dwarf = Race('Dwarf')

# Horde
orc = Race('Orc')
troll = Race('Troll')
tauren = Race('Tauren')
blood_elf = Race('Blood Elf')
undead = Race('Undead')

all = [gnome, night_elf, human, draenei, dwarf, orc, troll, tauren, blood_elf, undead]