import argparse
import asyncio
import subprocess
import sys

import config
from hardware.hal import get_hal, cleanup

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

hal = get_hal(configs["bike"])


overlay_process = None


def enable():
    print("ON")

    hal.display_power_led.turn_off()

    global overlay_process
    overlay_process = subprocess.Popen(
        [sys.executable, config.get_active_overlay(), "--host", brokerIP]
    )


def disable():
    print("OFF")

    hal.display_power_led.turn_on()

    global overlay_process
    if overlay_process:
        subprocess.Popen.kill(overlay_process)


async def main():
    try:
        if hal.display_power_switch.read() == switch_on_state:
            enable()

        while True:
            await hal.display_power_switch.wait_for_state(not switch_on_state)
            disable()

            await hal.display_power_switch.wait_for_state(switch_on_state)
            enable()

    except KeyboardInterrupt:
        if overlay_process:
            subprocess.Popen.kill(overlay_process)
        cleanup()


if __name__ == "__main__":
    asyncio.run(main())
