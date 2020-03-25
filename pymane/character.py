import pymane.races

from typing import List, Tuple

from pymane.arena_team import ArenaTeam
from pymane.guild import Guild
from pymane.log import get_logger
from pymane.page_cache import PageCache
from pymane.skill import Skill
from pymane.statistics import Statistics
from pymane.statistics.statistic import Statistic
from pymane.talents import TalentSpec

log = get_logger(__name__)

class CharacterNotFoundError(Exception):
	pass

class UnhandledParseError(Exception):
	pass

def is_highest_rating_statistic(value, description):
	return description is not None \
	       and value is not None \
	       and value.isdigit() \
	       and 'highest' in description.lower() \
	       and 'personal rating' in description.lower()

def _extract_level_race_class(info: str) -> Tuple[int, pymane.races.Race, str]:
	for race in pymane.races.all:
		if race.name in info:
			info = info.replace(race.name, '').split()
			return int(info[1]), race, info[2].replace(',', '')

	log.error(f'{info=}')
	raise UnhandledParseError('Level-race-class parse error')

class Character:
	def __init__(self, name: str, armory, realm_name: str = 'Icecrown'):
		self.__name = name
		self.__realm_name = realm_name
		self.__http = PageCache(http=armory.session.http)

	async def __character_does_not_exist(self, html):
		return html.find(text='Page not found') is not None

	async def total_hks(self) -> int:
		html = await self.__http.armory_get(f'character/{self.name()}/{self.__realm_name}/summary')
		if await self.__character_does_not_exist(html):
			raise CharacterNotFoundError(f'{self.name()} of {self.__realm_name} was not found')

		pvpbasic = html.select_one('.pvpbasic')
		if not pvpbasic:
			raise UnhandledParseError('pvpbasic Div not found')

		stubs = list(pvpbasic.select('.stub'))[0]
		return stubs.select_one('.text').span.text

	async def todays_hks(self) -> int:
		html = await self.__http.armory_get(f'character/{self.name()}/{self.__realm_name}/summary')
		if await self.__character_does_not_exist(html):
			raise CharacterNotFoundError(f'{self.name()} of {self.__realm_name} was not found')

		pvpbasic = html.select_one('.pvpbasic')
		if not pvpbasic:
			raise UnhandledParseError('pvpbasic Div not found')

		stubs = list(pvpbasic.select('.stub'))[1]
		return stubs.select_one('.text').span.text

	async def professions(self) -> List[Skill]:
		html = await self.__http.armory_get(f'character/{self.name()}/{self.__realm_name}/summary')
		if await self.__character_does_not_exist(html):
			raise CharacterNotFoundError(f'{self.name()} of {self.__realm_name} was not found')

		profskills = html.select_one('.profskills')
		if not profskills:
			return []

		stubs = list(profskills.select('.stub'))
		profs = [stub.select_one('.text').text.split() for stub in stubs]
		return [Skill(prof[0], int(prof[1]), int(prof[3])) for prof in profs]

	async def secondary_skills(self) -> List[Skill]:
		html = await self.__http.armory_get(f'character/{self.name()}/{self.__realm_name}/summary')
		if await self.__character_does_not_exist(html):
			raise CharacterNotFoundError(f'{self.name()} of {self.__realm_name} was not found')

		profskills = html.select('.profskills')[1]
		if not profskills:
			return []

		stubs = list(profskills.select('.stub'))
		profs = [stub.select_one('.text').text.split() for stub in stubs]
		return [Skill(' '.join(prof[0:len(prof) - 3]), int(prof[-3]), int(prof[-1])) for prof in profs]

	async def talent_specs(self) -> List[TalentSpec]:
		html = await self.__http.armory_get(f'character/{self.name()}/{self.__realm_name}/summary')
		if await self.__character_does_not_exist(html):
			raise CharacterNotFoundError(f'{self.name()} of {self.__realm_name} was not found')

		specialization = html.select_one('.specialization')
		if not specialization:
			return []

		stubs = list(specialization.select('.stub'))
		profs = [stub.select_one('.text').text.split() for stub in stubs]
		return [TalentSpec(' '.join(prof[0:len(prof) - 5]), int(prof[-5]), int(prof[-3]), int(prof[-1])) for prof in profs]

	async def _get_info_string(self):
		html = await self.__http.armory_get(f'character/{self.name()}/{self.__realm_name}/summary')
		if await self.__character_does_not_exist(html):
			raise CharacterNotFoundError(f'{self.name()} of {self.__realm_name} was not found')

		character_sheet = html.select_one('#character-sheet')
		if not character_sheet:
			return ''

		return character_sheet\
			.select_one('.information')\
			.select_one('.information-left')\
			.select_one('.level-race-class')\
			.text

	async def level(self) -> int:
		info = await self._get_info_string()
		level, _, _ = _extract_level_race_class(info)
		return level

	async def race(self) -> pymane.races.Race:
		info = await self._get_info_string()
		_, race, _ = _extract_level_race_class(info)
		return race

	async def player_class(self) -> str:
		info = await self._get_info_string()
		_, _, player_class = _extract_level_race_class(info)
		return player_class

	async def guild(self):
		html = await self.__http.armory_get(f'character/{self.name()}/{self.__realm_name}/summary')
		if await self.__character_does_not_exist(html):
			raise CharacterNotFoundError(f'{self.name()} of {self.__realm_name} was not found')

		pass

	def statistics(self) -> Statistics:
		return Statistics(character=self, http=self.__http)

	async def pvp_teams(self):
		html = await self.__http.armory_get(f'character/{self.name()}/{self.__realm_name}/summary')
		if await self.__character_does_not_exist(html):
			raise CharacterNotFoundError(f'{self.name()} of {self.__realm_name} was not found')

		pvpteams = html.select_one('.pvpteams')
		if not pvpteams:
			return []

		stubs = list(pvpteams.select('.stub'))
		teams = [stub.select_one('.text').text.split() for stub in stubs]
		return [ArenaTeam(name=' '.join(team[2:len(team) - 2]), rating=int(team[-2]), type=ArenaTeam.ArenaTeamType.parse(team[0])) for team in teams]

	async def highest_rating(self) -> Statistic:
		results = await self.statistics().category(pymane.statistics.categories.arena_pvp)
		ratings = [Statistic(value, description) for value, description in results if is_highest_rating_statistic(value, description)]
		sorted_ratings = sorted(ratings, key=lambda l: int(l.value), reverse=True)
		return sorted_ratings[0]

	def realm(self) -> str:
		return self.__realm_name

	def name(self) -> str:
		return self.__name
