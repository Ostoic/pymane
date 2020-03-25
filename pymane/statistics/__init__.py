import re
import html
from pymane.statistics.category import Category

categories = Category

def _process_value(value):
	if value == '- -':
		return None
	return value

class Statistics:
	def __init__(self, character, http):
		self.__character = character
		self.__http = http
		self.__field_pattern = re.compile('<td>(.+?)<\\\/td>[\\\\n]*\s*<td class=.+?>(.+?)<\\\/td>')

	async def category(self, category: Category):
		path = f'character/{self.__character.name()}/{self.__character.realm()}/statistics'
		response = await self.__http.armory_post(path, data={'category': category.value})
		result = html.unescape(str(response))

		return [(description, _process_value(value)) for description, value in self.__field_pattern.findall(result)]
