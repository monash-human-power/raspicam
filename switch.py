import argparse
import asyncio
import subprocess

import RPi.GPIO as gpio
import config

poll_frequency = 0.5
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

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)


class Switch:
    def __init__(self, pin):
        self.pin = pin
        gpio.setup(pin, gpio.IN, pull_up_down=gpio.PUD_UP)

    def read(self):
        return gpio.input(self.pin)

    async def wait_for_state(self, state):
        while True:
            if self.read() == state:
                return
            await asyncio.sleep(poll_frequency)


class LED:
    def __init__(self, pin):
        self.pin = pin
        gpio.setup(pin, gpio.OUT)

    def turn_on(self):
        gpio.output(self.pin, gpio.HIGH)

    def turn_off(self):
        gpio.output(self.pin, gpio.LOW)


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

            red_led.turn_on()
            green_led.turn_off()

    except KeyboardInterrupt:
        if overlay_process:
            subprocess.Popen.kill(overlay_process)
        gpio.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
