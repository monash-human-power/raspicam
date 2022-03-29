import argparse
import asyncio
import subprocess
import sys

import config
from utils.hardware import LED, Switch, use_board_pins, cleanup

switch_on_state = True

configs = config.read_configs()

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--host",
    type=str,
    default=configs["broker_ip"],
    help="ip address of the broker",
)
args = parser.parse_args()

brokerIP = args.host

use_board_pins()

switch = Switch(15)
green_led = LED(11)


overlay_process = None


def enable():
    print("ON")

    green_led.turn_off()

    global overlay_process
    overlay_process = subprocess.Popen(
        [sys.executable, config.get_active_overlay(), "--host", brokerIP]
    )


def disable():
    print("OFF")

    green_led.turn_on()

    global overlay_process
    if overlay_process:
        subprocess.Popen.kill(overlay_process)


async def main():
    try:
        if switch.read() == switch_on_state:
            enable()

        while True:
            await switch.wait_for_state(not switch_on_state)
            disable()

            await switch.wait_for_state(switch_on_state)
            enable()

    except KeyboardInterrupt:
        if overlay_process:
            subprocess.Popen.kill(overlay_process)
        cleanup()


if __name__ == "__main__":
    asyncio.run(main())
