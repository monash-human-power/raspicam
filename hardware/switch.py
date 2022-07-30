from abc import ABC, abstractmethod
import asyncio
from enum import Enum

from hardware.common import ON_PI

if ON_PI:
    import RPi.GPIO as gpio

    # Ignore warnings about multiple scripts playing with GPIO
    gpio.setwarnings(False)


poll_frequency = 0.5


class PullUpDown(Enum):
    OFF = "off"
    UP = "up"
    DOWN = "down"

    def to_gpio_value(self):
        if self == PullUpDown.OFF:
            return None
        elif self == PullUpDown.UP:
            return gpio.PUD_UP
        elif self == PullUpDown.DOWN:
            return gpio.PUD_DOWN


class Switch(ABC):
    @abstractmethod
    def __init__(self, pin: int, pull_up_down: PullUpDown):
        pass

    @abstractmethod
    def read(self) -> bool:
        pass

    async def wait_for_state(self, state: bool):
        while True:
            if self.read() == state:
                return
            await asyncio.sleep(poll_frequency)

    @abstractmethod
    def create_interrupt(self, callback, bouncetime=500):
        pass


class PhysicalSwitch(Switch):
    def __init__(self, pin: int, pull_up_down: PullUpDown):
        self.pin = pin
        gpio.setup(pin, gpio.IN, pull_up_down=pull_up_down.to_gpio_value())

    def read(self) -> bool:
        return gpio.input(self.pin)

    def create_interrupt(self, callback, bouncetime=500):
        gpio.add_event_detect(
            self.pin, gpio.RISING, callback=callback, bouncetime=bouncetime
        )


class DummySwitch(Switch):
    def __init__(self, pin: int, pull_up_down: PullUpDown):
        self.pin = pin
        self.pin_state = False

    def read(self) -> bool:
        return self.pin_state

    def create_interrupt(self, callback, bouncetime=500):
        print(
            f"Creating dummy interrupt for pin {self.pin}. Callback will not be called."
        )


class NopSwitch(ABC):
    def __init__(self, pin, pull_up_down):
        pass

    def read(self):
        pass

    async def wait_for_state(self, state):
        pass

    def create_interrupt(self, callback, bouncetime=500):
        pass


def init_switch(pin: int, pull_up_down: PullUpDown = PullUpDown.UP) -> Switch:
    if ON_PI:
        return PhysicalSwitch(pin, pull_up_down)
    else:
        return DummySwitch(pin, pull_up_down)
