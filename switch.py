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

# Pins
switch = 15
green_led = 11
red_led = 13

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

gpio.setup(switch, gpio.IN, pull_up_down=gpio.PUD_UP)  # toggle switch
gpio.setup(green_led, gpio.OUT)  # green LED
gpio.setup(red_led, gpio.OUT)


def turn_on(led):
    gpio.output(led, gpio.HIGH)


def turn_off(led):
    gpio.output(led, gpio.LOW)


try:
    while True:
        prev_switch_state = gpio.input(15)
        while True:
            turn_on(red_led)
            switch_state = gpio.input(15)
            if switch_state == prev_switch_state:
                print("OFF")
            else:
                print("ON")
                break
            sleep(0.25)
        prev_switch_state = switch_state
        # TODO: Remove hard coding of directory of python script
        p1 = subprocess.Popen(
            ["python3", config.get_active_overlay(), "--host", brokerIP]
        )
        turn_off(red_led)
        turn_on(green_led)
        sleep(1)

        while True:
            switch_state = gpio.input(15)
            if switch_state != prev_switch_state:
                print("OFF")
                subprocess.Popen.kill(p1)
                turn_off(green_led)
                break
            else:
                print("ON")
            sleep(1)
            prev_switch_state = switch_state

except KeyboardInterrupt:
    subprocess.Popen.kill(p1)
    gpio.cleanup()
