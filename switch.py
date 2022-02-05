import argparse
import subprocess
from time import sleep

import RPi.GPIO as gpio
import config

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

try:
    while True:
        prev_switch_state = switch.read()
        while True:
            red_led.turn_on()
            switch_state = switch.read()
            if switch_state == prev_switch_state:
                print("OFF")
            else:
                print("ON")
                break
            sleep(0.25)
        prev_switch_state = switch_state
        # TODO: Remove hard coding of directory of python script
        p1 = subprocess.Popen(
            [
                f"{virtualenv_dir}/bin/python",
                config.get_active_overlay(),
                "--host",
                brokerIP,
            ]
        )
        red_led.turn_off()
        green_led.turn_on()
        sleep(1)

        while True:
            switch_state = switch.read()
            if switch_state != prev_switch_state:
                print("OFF")
                subprocess.Popen.kill(p1)
                green_led.turn_off()
                break
            else:
                print("ON")
            sleep(1)
            prev_switch_state = switch_state

except KeyboardInterrupt:
    subprocess.Popen.kill(p1)
    gpio.cleanup()
