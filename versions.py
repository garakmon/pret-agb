import map_names
import charmap

firered = {
	'version': 'firered',
	'map_groups_address': ,
	'baserom_path': 'baserom.gba',
	'maps_paths': ['data/event_scripts.s', 'data/rom4.s', 'data/graphics.s', 'data/sound_data.s', 'data/rom_8525F58.s', 'data/battle_frontier_2.s'],
	'force_stop_addresses': [],
	'map_names': map_names.firered,
	'field_object_constants_path': 'constants/map_object_constants.inc',
	'battle_frontier_constants_path': 'constants/battle_frontier_constants.inc',
	'charmap': charmap.emerald_decode,
	'charmap_jp': charmap.emerald_jp_decode,
	'mapfile': 'pokeemerald.map',
}

emerald = {
	'version': 'emerald',
	'map_groups_address': 0x486578,
	'baserom_path': 'baserom.gba',
	'maps_paths': ['data/event_scripts.s', 'data/rom4.s', 'data/graphics.s', 'data/sound_data.s', 'data/rom_8525F58.s', 'data/battle_frontier_2.s'],
	'force_stop_addresses': [
		0x209a99, # SlateportCityBattleTent waitstate
		0x2c8381, # TrainerHill1F missing end
	],
	'map_names': map_names.emerald,
	'field_object_constants_path': 'constants/map_object_constants.inc',
	'battle_frontier_constants_path': 'constants/battle_frontier_constants.inc',
	'charmap': charmap.emerald_decode,
	'charmap_jp': charmap.emerald_jp_decode,
	'mapfile': 'pokeemerald.map',
}

ruby = {
	'version': 'ruby',
	'map_groups_address': 0x308588,
	'baserom_path': 'baserom.gba',
	'maps_paths': [
		'data/data1.s', 'data/data2.s', 'data/graphics.s', 'data/sound_data.s', 'asm/crt0.s', 'asm/rom1.s', 'asm/rom2.s', 'asm/rom3.s', 'asm/rom4.s', 'asm/rom5.s', 'asm/libgcnmultiboot.s', 'asm/m4a_1.s', 'asm/m4a_3.s', 'asm/libagbsyscall.s', 'asm/libc.s',
		'data/event_scripts.s', 'data/battle_ai_scripts.s',
	],
	'force_stop_addresses': [],
	'map_names': map_names.ruby,
	'field_object_constants_path': 'constants/map_object_constants.s',
	'charmap': charmap.ruby_decode,
	'charmap_jp': charmap.ruby_jp_decode,
	'mapfile': 'pokeruby.map',
}

sapphire = {
	'version': 'sapphire',
	'map_groups_address': 0x308518,
	'baserom_path': 'baserom_sapphire.gba',
	'maps_paths': [
		'data/data1.s', 'data/data2.s', 'data/graphics.s', 'data/sound_data.s', 'asm/crt0.s', 'asm/rom1.s', 'asm/rom2.s', 'asm/rom3.s', 'asm/rom4.s', 'asm/rom5.s', 'asm/libgcnmultiboot.s', 'asm/m4a_1.s', 'asm/m4a_3.s', 'asm/libagbsyscall.s', 'asm/libc.s',
		'data/event_scripts.s', 'data/battle_ai_scripts.s',
	],
	'force_stop_addresses': [],
	'map_names': map_names.ruby,
	'field_object_constants_path': 'constants/map_object_constants.s',
	'charmap': charmap.ruby_decode,
	'charmap_jp': charmap.ruby_jp_decode,
	'mapfile': 'pokesapphire.map',
}
