from enum import Enum

class Category(Enum):
	summary = 'summary'
	# Character
	character = 130
	wealth = 140
	consumables = 145
	reputation = 147
	gear = 191

	# Combat
	combat = 141

	# Kills
	kills = 128
	creature_kills = 135
	honor_kills = 136
	killing_blows = 137

	# Deaths
	deaths = 122
	arena_deaths = 123
	battleground_deaths = 124
	dungeon_deaths = 125
	world_deaths = 126
	resurrection = 127

	# Quests
	quests = 133

	# Dungeons and Raids
	pve = 14807
	classic_pve = 14821
	tbc_pve = 14822
	wotlk_pve = 14823
	ulduar_pve = 14963
	toc_pve = 15021
	icc_pve = 15062

	# Skills
	skills = 132
	secondary_skills = 178
	professions = 173

	# Travel
	travel = 134

	# Social
	social = 131

	# PvP
	pvp = 21
	arena_pvp = 152
	battleground_pvp = 153
	world_pvp = 154