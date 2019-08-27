import os
import json
import fnmatch
from dotenv import load_dotenv

load_dotenv()
CONFIG_FILE = 'configs.json'
ACTIVE_OVERLAY_KEY = 'activeOverlay'
OVERLAY_FILE_PATTERN = 'overlay_*.py'
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def get_overlays(directory=CURRENT_DIRECTORY):
	overlays = [file for file in os.listdir(directory) if fnmatch.fnmatch(file, OVERLAY_FILE_PATTERN)]
	return overlays


def set_overlay(new_overlays, directory=CURRENT_DIRECTORY):
	current_device = os.getenv('MHP_CAMERA')
	new_overlay = new_overlays[current_device]

	configs = read_configs(directory)
	if 'device' in configs:
		configs.pop('device')
	configs[ACTIVE_OVERLAY_KEY] = new_overlay

	with open(os.path.join(directory, CONFIG_FILE), 'w') as f:
		json.dump(configs, f, indent=2, sort_keys=True)


def read_configs(directory=CURRENT_DIRECTORY):
	filepath = os.path.join(directory, CONFIG_FILE)
	if not os.path.isfile(filepath):
		return {}
	else:
		with open(filepath) as f:
			configs = json.load(f)

			current_device = os.getenv('MHP_CAMERA')
			configs['device'] = current_device
			configs['overlays'] = get_overlays()
			return configs


def get_active_overlay(directory=CURRENT_DIRECTORY):
	configs = read_configs(directory)
	return os.path.join(directory, configs[ACTIVE_OVERLAY_KEY])


if __name__ == '__main__':
	# set_overlay({'primary': 'Overlay_Demo2.py'})
	# print(get_active_overlay())
	print(json.dumps(read_configs()))
