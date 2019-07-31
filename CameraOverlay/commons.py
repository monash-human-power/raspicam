import os
import json
import fnmatch

OVERLAY_FILE_PATTERN = 'Overlay_Demo*.py'
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def get_overlays(dir=CURRENT_DIRECTORY):
	overlays = [os.path.basename(file) for file in os.listdir(dir) if fnmatch.fnmatch(file, OVERLAY_FILE_PATTERN)]
	return overlays


def set_overlay(overlay, dir=CURRENT_DIRECTORY):
	with open(os.path.join(dir, 'configs.json'), 'w') as f:
		json.dump({'activeOverlay': overlay}, f, indent=2)


if __name__ == '__main__':
	print(get_overlays())
	set_overlay('test')
