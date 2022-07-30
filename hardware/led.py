from abc import ABC, abstractmethod

from hardware.common import ON_PI

if ON_PI:
    import RPi.GPIO as gpio

    gpio.setmode(gpio.BCM)
    # Ignore warnings about multiple scripts playing with GPIO
    gpio.setwarnings(False)


class LED(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class PhysicalLED(LED):
    def __init__(self, pin: int):
        self.pin = pin
        gpio.setup(pin, gpio.OUT)

    def turn_on(self):
        gpio.output(self.pin, gpio.HIGH)

    def turn_off(self):
        gpio.output(self.pin, gpio.LOW)


class DummyLED(LED):
    def __init__(self, pin: int):
        self.pin = pin

    def turn_on(self):
        print(f"LED at pin {self.pin} set to on")

    def turn_off(self):
        print(f"LED at pin {self.pin} set to off")


class NopLED(LED):
    def turn_on(self):
        pass

    def turn_off(self):
        pass


def init_led(pin: int) -> LED:
    if ON_PI:
        return PhysicalLED(pin)
    else:
        return DummyLED(pin)
