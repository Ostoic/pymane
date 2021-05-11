import functools
import inspect
from contextlib import asynccontextmanager, contextmanager

import requests
import requests_random_user_agent
import trio

from .armory import Armory

class Session:
	def __init__(self, http, *args, **kwargs):
		self.http = http
		self.options = kwargs
		self.armory = Armory(session=self)

		async def _request_threaded(*args, **kwargs):
			return await trio.to_thread.run_sync(functools.partial(self.http.request, *args, **kwargs))

		self._request = self.http.request if inspect.iscoroutinefunction(self.http.request) else _request_threaded

	async def request(self, request: str, url: str, *args, **kwargs):
		return  await self._request(request, url, *args, **kwargs)

	async def get(self, url: str, *args, **kwargs):
		return await self.request('GET', url, *args, **kwargs)

	async def post(self, url: str, *args, **kwargs):
		return await self.request('POST', url, *args, **kwargs)

@contextmanager
def connect(proxies=None, *args, **kwargs) -> Session:
	http = requests.Session()

	if proxies is not None:
		http.proxies.update(proxies)

	try:
		session = Session(http, *args, **kwargs)
		yield session

	finally:
		http.close()

