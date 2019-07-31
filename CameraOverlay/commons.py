import os
import json
from dotenv import load_dotenv

load_dotenv()
CONFIG_FILE = 'configs.json'
ACTIVE_OVERLAY_KEY = 'activeOverlay'
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def set_overlay(new_overlays, dir=CURRENT_DIRECTORY):
	current_device = os.getenv('MHP_CAMERA')
	new_overlay = new_overlays[current_device]

	configs = read_configs(dir)
	if 'device' in configs:
		configs.pop('device')
	configs[ACTIVE_OVERLAY_KEY] = new_overlay

	with open(os.path.join(dir, CONFIG_FILE), 'w') as f:
		json.dump(configs, f, indent=2, sort_keys=True)

def read_configs(dir=CURRENT_DIRECTORY):
	filepath = os.path.join(dir, CONFIG_FILE)
	if not os.path.isfile(filepath):
		return {}
	else:
		with open(filepath) as f:
			configs = json.load(f)

			current_device = os.getenv('MHP_CAMERA')
			configs['device'] = current_device
			return configs

def get_active_overlay(dir=CURRENT_DIRECTORY):
	configs = read_configs(dir)
	return os.path.join(dir, configs[ACTIVE_OVERLAY_KEY])

if __name__ == '__main__':
	set_overlay({'primary': 'Overlay_Demo2.py'})
	print(get_active_overlay())
	print(read_configs())
