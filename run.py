import pymane
import trio

async def run():
	players = [('Act', 'Icecrown'), ('Banditwarr', 'Blackrock'), ('Devastators', 'Blackrock')]
	async with pymane.connect() as warmane:
		chars = [warmane.armory.character(name, realm=realm) for name, realm in players]
		for char in chars:
			try:
				print(f'bongour: {char.name()}')
				print(f'Character: {char.name()}, level {await char.level()} {await char.race()} {await char.player_class()}, {char.realm()}')
				print(f'Total hks: {await char.total_hks()}, today\'s hks: {await char.todays_hks()}')
				print(f'Professions: {list(await char.professions())}')
				print(f'Skills: {list(await char.secondary_skills())}')
				print(f'Specs: {list(await char.talent_specs())}')
				print(f'Arena teams: {list(await char.pvp_teams())}')
				for description, value in await char.statistics().category(pymane.statistics.categories.killing_blows):
					print(f'Statistic: {value=}, {description=}')
				print(f'Highest arena reating: {await char.highest_rating()}')
			except Exception as e:
				print(f'Error: {e}')
				pass

# characters, guilds, teams = await warmane.armory.search()

if __name__ == '__main__':
	trio.run(run)
