import os
import json
import fnmatch

CONFIG_FILE = 'configs.json'
ACTIVE_OVERLAY_KEY = 'activeOverlay'
OVERLAY_FILE_PATTERN = 'Overlay_Demo*.py'
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def get_overlays(dir=CURRENT_DIRECTORY):
	overlays = [os.path.basename(file) for file in os.listdir(dir) if fnmatch.fnmatch(file, OVERLAY_FILE_PATTERN)]
	return overlays


def set_overlay(overlay, dir=CURRENT_DIRECTORY):
	with open(os.path.join(dir, CONFIG_FILE), 'w') as f:
		json.dump({ACTIVE_OVERLAY_KEY: overlay}, f, indent=2)

def get_active_overlay(dir=CURRENT_DIRECTORY):
	with open(os.path.join(dir, CONFIG_FILE)) as f:
		data = json.load(f)
		active_overlay = data[ACTIVE_OVERLAY_KEY]
		return os.path.join(dir, active_overlay)

if __name__ == '__main__':
	print(get_overlays())
	set_overlay('bleh bleh bleh')
	print(get_active_overlay())
