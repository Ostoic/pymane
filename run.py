import pymane
import asyncio

async def run():
	players = [('Act', 'Icecrown'), ('Banditwarr', 'Blackrock'), ('Devastators', 'Blackrock')]
	async with pymane.connect() as warmane:
		chars = [warmane.armory.character(name, realm=realm) for name, realm in players]
		for char in chars:
			try:
				print(f'Character: {char.name()}, level {await char.level()} {await char.race()} {await char.player_class()}, {char.realm()}')
				print(f'Total hks: {await char.total_hks()}, today\'s hks: {await char.todays_hks()}')
				print(f'Professions: {list(await char.professions())}')
				print(f'Skills: {list(await char.secondary_skills())}')
				print(f'Specs: {list(await char.talent_specs())}')
				print(f'Arena teams: {list(await char.pvp_teams())}')
				print(await char.highest_rating())
				from pprint import pprint
				# pprint(kbs)
				# return
			except Exception as e:
				print(f'Error: {str(e)}')
				pass


# characters, guilds, teams = await warmane.armory.search()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run())
	# loop.run_forever()