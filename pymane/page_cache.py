import time
import bs4

from pymane.log import get_logger

log = get_logger('pymane.page_cache')

class PageCache:
	def __init__(self, http):
		self.__http = http
		self.__request_history = {}
		self.__store_duration = 10

	async def make_request(self, path: str, request: str = 'GET', **kwargs):
		hashed_request = hash((path, request, frozenset(kwargs.keys())))
		if hashed_request not in self.__request_history or (time.time() - self.__request_history[hashed_request][1]) > self.__store_duration:
			log.debug(f'New \'{request}\' request for: {path}')
			self.__request_history[hashed_request] = \
				(await self.__http.request(request, path, **kwargs), time.time())

		return bs4.BeautifulSoup(await self.__request_history[hashed_request][0].text(), 'html.parser')

	async def get(self, path: str):
		return await self.make_request(path, 'GET')

	async def armory_get(self, path: str):
		return await self.get(f'http://armory.warmane.com/{path}')

	async def post(self, path: str, **kwargs):
		return await self.make_request(path, request='POST', **kwargs)

	async def armory_post(self, path: str, **kwargs):
		return await self.post(f'http://armory.warmane.com/{path}', **kwargs)