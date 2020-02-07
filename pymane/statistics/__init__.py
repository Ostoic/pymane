import re
import html

from aiohttp import FormData
from pymane.statistics.category import Category

categories = Category

class Statistics:
	def __init__(self, character, http):
		self.__character = character
		self.__http = http
		self.__field_pattern = re.compile('<td>(.+?)<\\\/td>[\\\\n]*\s*<td class=.+?>(.+?)<\\\/td>')

	async def category(self, category: Category):
		path = f'character/{self.__character.name()}/{self.__character.realm()}/statistics'
		data = FormData(fields=[('category', category.value)])
		response = await self.__http.armory_post(path, data=data)
		result = html.unescape(str(response))

		return self.__field_pattern.findall(result)
