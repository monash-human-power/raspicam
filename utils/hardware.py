import asyncio
import RPi.GPIO as gpio


poll_frequency = 0.5


# Ignore warnings about multiple scripts playing with GPIO
gpio.setwarnings(False)


def use_board_pins():
    gpio.setmode(gpio.BOARD)


def cleanup():
    gpio.cleanup()


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
