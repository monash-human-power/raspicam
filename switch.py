import argparse
import asyncio
import subprocess

import config
from utils.hardware import LED, Switch, use_board_pins

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
red_led = LED(13)


virtualenv_dir = (
    subprocess.check_output(["poetry", "env", "info", "-p"])
    .decode("utf-8")
    .strip()
)
print("env dir:", virtualenv_dir)


async def main():
    overlay_process = None
    try:
        while True:
            await switch.wait_for_state(not switch_on_state)
            print("OFF")

            red_led.turn_on()
            green_led.turn_off()

            if overlay_process:
                subprocess.Popen.kill(overlay_process)

            await switch.wait_for_state(switch_on_state)
            print("ON")

            red_led.turn_off()
            green_led.turn_on()

            overlay_process = subprocess.Popen(
                [
                    f"{virtualenv_dir}/bin/python",
                    config.get_active_overlay(),
                    "--host",
                    brokerIP,
                ]
            )

    except KeyboardInterrupt:
        if overlay_process:
            subprocess.Popen.kill(overlay_process)
        gpio.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
