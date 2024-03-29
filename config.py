"""Helper functions for editing configuration file"""
import fnmatch
import json
import os
import random
from warnings import warn

from dotenv import load_dotenv

load_dotenv()
CONFIG_FILE = "configs.json"
ACTIVE_OVERLAY_KEY = "activeOverlay"
OVERLAY_FILE_PATTERN = "overlay_*.py"
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

ROTATION_KEY = "rotation"

DEFAULT_BROKER_IP = "192.168.100.100"
DEFAULT_BIKE = "V3"
DEFAULT_VIEWPORT_SIZE = [1024, 600]

BATTERY_PUBLISH_INTERVAL = 5 * 60  # seconds


def get_overlays(directory=CURRENT_DIRECTORY):
    """Get overlays stored in directory"""
    overlays = [
        file
        for file in os.listdir(directory)
        if fnmatch.fnmatch(file, OVERLAY_FILE_PATTERN)
    ]
    return overlays


def set_overlay(new_overlays, directory=CURRENT_DIRECTORY):
    """Set current camera overlay"""
    current_device = os.getenv("MHP_CAMERA")
    new_overlay = new_overlays[current_device]

    configs = read_configs(directory)
    if "device" in configs:
        configs.pop("device")
    configs[ACTIVE_OVERLAY_KEY] = new_overlay

    with open(os.path.join(directory, CONFIG_FILE), "w") as file:
        json.dump(configs, file, indent=2, sort_keys=True)


def set_rotation(rotation, directory=CURRENT_DIRECTORY):
    """Set rotation for device"""
    configs = read_configs(directory)
    if "device" in configs:
        configs.pop("device")
    configs[ROTATION_KEY] = rotation

    with open(os.path.join(directory, CONFIG_FILE), "w") as file:
        json.dump(configs, file, indent=2, sort_keys=True)


def read_configs(directory=CURRENT_DIRECTORY):
    """Read config.json file"""
    configs_file = os.path.join(directory, CONFIG_FILE)

    if not os.path.isfile(configs_file):
        create_default_configs(directory)

    with open(configs_file) as file:
        configs = json.load(file)

    if ACTIVE_OVERLAY_KEY not in configs:
        create_default_configs(directory)
        with open(configs_file) as file:
            configs = json.load(file)

    configs["device"] = os.getenv("MHP_CAMERA")
    if not configs["device"]:
        warn("MHP_CAMERA has not been set in .env")

    configs["bike"] = os.getenv("MHP_BIKE")
    if not configs["bike"]:
        warn(f"MHP_BIKE is not set in .env, defaulting to {DEFAULT_BIKE}")
        configs["bike"] = DEFAULT_BIKE

    configs["broker_ip"] = os.getenv("BROKER_IP")
    if not configs["broker_ip"]:
        warn(
            f"BROKER_IP is not set in .env, defaulting to {DEFAULT_BROKER_IP}"
        )
        configs["broker_ip"] = DEFAULT_BROKER_IP

    try:
        # Transform env var string "1280,740" into int tuple (1280, 740)
        configs["viewport_size"] = tuple(
            map(int, os.getenv("VIEWPORT_SIZE").split(","))
        )
    except AttributeError:
        warn(
            "VIEWPORT_SIZE is not set in .env, "
            + f"defaulting to {DEFAULT_VIEWPORT_SIZE}"
        )
        configs["viewport_size"] = DEFAULT_VIEWPORT_SIZE
    except ValueError:
        warn(
            f"VIEWPORT_SIZE '{os.getenv('VIEWPORT_SIZE')}' in .env is invalid,"
            + f" defaulting to {DEFAULT_VIEWPORT_SIZE}"
        )
        configs["viewport_size"] = DEFAULT_VIEWPORT_SIZE

    if len(configs["viewport_size"]) != 2:
        warn(
            "VIEWPORT_SIZE must contain exactly two integers, "
            + f"defaulting to {DEFAULT_VIEWPORT_SIZE}"
        )
        configs["viewport_size"] = DEFAULT_VIEWPORT_SIZE

    configs["overlays"] = get_overlays()
    return configs


def create_default_configs(directory):
    """Create a default config file"""
    random_overlay = random.choice(get_overlays(directory))
    with open(os.path.join(directory, CONFIG_FILE), "w") as file:
        json.dump(
            {ACTIVE_OVERLAY_KEY: random_overlay},
            file,
            indent=2,
            sort_keys=True,
        )
    return random_overlay


def get_active_overlay(directory=CURRENT_DIRECTORY):
    """Get the current active overlay"""
    configs = read_configs(directory)
    try:
        active_overlay = configs[ACTIVE_OVERLAY_KEY]
    except KeyError:
        active_overlay = create_default_configs(directory)
    return os.path.join(directory, active_overlay)


if __name__ == "__main__":
    # set_overlay({'primary': 'overlay_all_stats.py'})
    # print(get_active_overlay())
    print(json.dumps(read_configs()))
