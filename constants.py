# coding: utf-8

from os.path import exists

def find_labels(path):
	labels = {}
	if not exists(path):
		return labels
	lines = open(path).readlines()
	for line in lines:
		if '.include' in line:
			incpath = line.split('"')[1]
			labels.update(find_labels(incpath))
		elif ': @' in line:
			i = line.find(':')
			j = line.find('@', i) + 1
			try:
				label, address = line[:i], int(line[j:].split()[0], 16)
				labels[address] = label
			except:
				pass
	return labels

def read_mapfile(path):
	"""This is way simpler..."""
	labels = {}
	try:
		lines = open(path).readlines()
	except:
		return labels
	for line in open(path):
		parts = line.split(' ' * 16)
		if len(parts) > 2:
			label = parts[2].strip()
			if '=' in label.split() or '.' in label.split():
				continue
			address = int(parts[1], 0)
			if address & 0x02000000:
				labels[address] = label
			elif address & 0x08000000:
				labels[address] = label
	return labels

def load_rom(filename):
	return bytearray(open(filename, 'rb').read())

def read_map_groups(path, map_names):
	lines = open(path).readlines()
	variables = {}
	maps = {}
	map_constants = {}
	for line in lines:
		line = line.strip()
		if line.startswith('.set'):
			name, value = line.split('.set')[1].split(',')
			variables[name.strip()] = int(value, 0)
		elif line.startswith('new_map_group'):
			variables['cur_map_group'] += 1
			variables['cur_map_num'] = 0
			map_constants[variables['cur_map_group']] = {}
			maps[variables['cur_map_group']] = {}
		elif line.startswith('map_group'):
			text = line.split('map_group')[1]
			group, num = map(variables.get, ['cur_map_group','cur_map_num'])
			name = text.split()[0]
			map_constants[group][num] = name
			variables['cur_map_num'] += 1

	i = 0
	for group_num, group in map_constants.items():
		for map_num, name in group.items():
			new_name = map_names[i]
			maps[group_num][map_num] = new_name
			i += 1

	return maps, map_constants

def get_map_name(map_groups, group, num):
	try:
		return map_groups[group][num]
	except:
		return None

def read_constants(path):
	variables = {}
	try:
		lines = open(path).readlines()
	except:
		return variables

	for line in lines:
		line = line.split('@')[0].strip()
		if line.startswith('.set'):
			name, value = line.split('.set')[1].split(',')
			if '<<' in value: # not supported yet
				pass
			else:
				value = value.strip()
				if value in variables.keys():
					value = variables[value]
				else:
					value = int(value, 0)
				variables[name.strip()] = value
		elif line.startswith('.equiv'):
			name, value = line.split('.equiv')[1].split(',')
			if '<<' in value: # not supported yet
				pass
			else:
				value = value.strip()
				if value in variables.keys():
					value = variables[value]
				else:
					if value.startswith('(') and value.endswith(')'):
						value = value[1:-1]
					try:
						value = int(value, 0)
					except ValueError:
						pieces = [x.strip() for x in value.split('+')]
						value = 0
						for x in pieces:
							if x in variables.keys():
								value += variables[x]
							else:
								value += int(x, 0)
				variables[name.strip()] = value

		elif line.startswith('enum_start'):
			try:
				enum = int(line.split('enum_start')[1], 0)
			except ValueError:
				enum = 0
		elif line.startswith('enum'):
			name = line.split('enum')[1].strip()
			variables[name] = enum
			enum += 1

	return variables

def reverse_constants(variables):
	return {v:k for k,v in variables.items()}

def read_reverse_constants(path):
	return reverse_constants(read_constants(path))

def read_specials(path):
	specials = []
	try:
		lines = open(path).readlines()
	except:
		return specials

	for line in lines:
		if line.strip().startswith('def_special'):
			label = line.split('def_special')[1].strip()
			specials += [label]
	return specials

def setup_version(version):
	if version.has_key('baserom_path'):
		version['baserom'] = load_rom(version['baserom_path'])
	if version.has_key('map_names'):
		version['map_groups'], version['map_constants'] = read_map_groups('constants/map_constants.inc', version['map_names'])
	version.update({
		'pokemon_constants': read_reverse_constants('constants/species_constants.inc'),
		'item_constants': read_reverse_constants('constants/item_constants.inc'),
		'trainer_constants': {
			v: k for k, v in read_constants('constants/trainer_constants.inc').items()
			if k.startswith('TRAINER_')
			and not k.startswith('TRAINER_PIC_')
			and not k.startswith('TRAINER_CLASS_')
			and not k.startswith('TRAINER_CLASS_NAME_')
			and not k.startswith('TRAINER_ENCOUNTER_MUSIC_')
		},
		'move_constants': read_reverse_constants('constants/move_constants.inc'),
		'song_constants': read_reverse_constants('constants/songs.inc'),
		'battle_text_constants': read_reverse_constants('constants/battle_text.inc'),
		'ability_constants': read_reverse_constants('constants/ability_constants.inc'),
		'type_constants': read_reverse_constants('constants/type_constants.inc'),
		'move_effect_constants': read_reverse_constants('constants/battle_move_effects.inc'),
		'hold_effect_constants': read_reverse_constants('constants/hold_effects.inc'),
		'specials': read_specials(version.get('specials_path', 'data/specials.inc')),
		'variables': read_reverse_constants('constants/variables.inc'),
		'flags': read_reverse_constants('constants/flags.inc'),
	})

	if version.get('mapfile'):
		version['labels'] = read_mapfile(version.get('mapfile'))
	else:
		version['labels'] = {}
		for path in version.get('maps_paths', []):
			version['labels'].update(find_labels(path))

	path = version.get('frontier_item_constants_path')
	if path:
		version['frontier_item_constants'] = {
			v: k for k, v in read_constants(path).items()
			if k.startswith('BATTLE_FRONTIER_ITEM_')
		}
	path = version.get('field_object_constants_path')
	if path:
		version['field_object_constants'] = {
			v: k for k, v in read_constants(path).items()
			if k.startswith('FIELD_OBJ_GFX_')
			or k.startswith('MAP_OBJ_GFX_')
		}
