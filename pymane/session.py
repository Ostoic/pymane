import aiohttp
from .armory import Armory

class Session:
	def __init__(self):
		self.http = aiohttp.ClientSession()
		self.armory = Armory(session=self)

	async def close(self):
		await self.http.close()

	async def __aenter__(self):
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		await self.close()

def connect() -> Session:
	return Session()