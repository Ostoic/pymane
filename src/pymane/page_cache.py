import bs4
import datetime

from .error import CaptchaRequiredError
from .log import get_logger

log = get_logger(__name__)

def new_proxy(address: str) -> dict:
	return dict(http=address, https=address)

class PageCache:
	def __init__(self, http):
		self.__http = http
		self.__request_history = {}
		self.__store_duration = datetime.timedelta(seconds=30)

	async def request(self, path: str, request: str = 'GET', *args, **kwargs):
		hashed_request = hash((path, request, frozenset(kwargs.keys())))
		if hashed_request not in self.__request_history or (datetime.datetime.now() - self.__request_history[hashed_request][1]) > self.__store_duration:
			log.debug(f'New \'{request}\' request for: {path}')
			html = await self.__http.request(request, path, *args, **kwargs)
			if html is None:
				raise ValueError(f'{html=}')

			# Make sure not to cache captcha responses
			if ' | Cloudflare' in html.text:
				raise CaptchaRequiredError()

			self.__request_history[hashed_request] = (html, datetime.datetime.now())

		return bs4.BeautifulSoup(self.__request_history[hashed_request][0].text, 'html.parser')

	async def get(self, path: str):
		return await self.request(path, request='GET')

	async def armory_get(self, path: str):
		return await self.get(f'http://armory.warmane.com/{path}')

	async def post(self, path: str, *args, **kwargs):
		return await self.request(path, request='POST', *args, **kwargs)

	async def armory_post(self, path: str, *args, **kwargs):
		return await self.post(f'http://armory.warmane.com/{path}', *args, **kwargs)