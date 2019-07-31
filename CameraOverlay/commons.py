import os
import fnmatch

OVERLAY_FILE_PATTERN = 'Overlay_Demo*.py'
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def get_overlays(dir=CURRENT_DIRECTORY):
	overlays = [file for file in os.listdir(dir) if fnmatch.fnmatch(file, OVERLAY_FILE_PATTERN)]
	return overlays

if __name__ == '__main__':
    print(get_overlays('./CameraOverlay/'))
