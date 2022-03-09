import asyncio
import RPi.GPIO as gpio
import time


poll_frequency = 0.5


# Ignore warnings about multiple scripts playing with GPIO
gpio.setwarnings(False)


def use_board_pins():
    gpio.setmode(gpio.BOARD)


def cleanup():
    gpio.cleanup()


class Switch:
    def __init__(self, pin, pull_up_down=gpio.PUD_UP):
        self.pin = pin
        self.last_interrupt_time = time.time()
        self.debounce_period = 0.5
        gpio.setup(pin, gpio.IN, pull_up_down=pull_up_down)

    def read(self):
        return gpio.input(self.pin)

    async def wait_for_state(self, state):
        while True:
            if self.read() == state:
                return
            await asyncio.sleep(poll_frequency)

    def _interrupt_callback(self, _pin_number):
        time_since_interrupt = time.time() - self.last_interrupt_time
        self.last_interrupt_time = time.time()
        if self.debounce and time_since_interrupt > self.debounce_period:
            self.callback()

    def create_interrupt(self, callback, debounce=True):
        self.callback = callback
        self.debounce = debounce
        gpio.add_event_detect(self.pin, gpio.RISING, callback=self._interrupt_callback)


class LED:
    def __init__(self, pin):
        self.pin = pin
        gpio.setup(pin, gpio.OUT)

    def turn_on(self):
        gpio.output(self.pin, gpio.HIGH)

    def turn_off(self):
        gpio.output(self.pin, gpio.LOW)
