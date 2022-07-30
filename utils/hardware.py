from abc import ABC, abstractmethod
import asyncio
from enum import Enum

try:
    import RPi.GPIO as gpio

    # Ignore warnings about multiple scripts playing with GPIO
    gpio.setwarnings(False)

    ON_PI = True
except (ImportError, RuntimeError):
    ON_PI = False


poll_frequency = 0.5


def use_board_pins():
    gpio.setmode(gpio.BOARD)


def cleanup():
    if ON_PI:
        gpio.cleanup()


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


class LED(ABC):
    @abstractmethod
    def __init__(self, pin: int):
        pass

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
    def __init__(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass


def init_led(pin: int) -> LED:
    if ON_PI:
        return PhysicalLED(pin)
    else:
        return DummyLED(pin)


class HardwareAbstractionLayer(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @property
    @abstractmethod
    def display_power_led(self) -> LED:
        pass

    @property
    @abstractmethod
    def mqtt_connected_led(self) -> LED:
        pass

    @property
    @abstractmethod
    def logging_led(self) -> LED:
        pass

    @property
    @abstractmethod
    def logging_button(self) -> Switch:
        pass

    @property
    @abstractmethod
    def display_power_switch(self) -> Switch:
        pass


class V2HAL(HardwareAbstractionLayer):
    def __init__(self):
        self._display_power_led = init_led(17)  # board pin 11, green led
        self._mqtt_connected_led = NopLED()  # LED not present on V2
        self._logging_led = init_led(27)  # board pin 13, red led
        self._logging_button = NopSwitch()  # Button not present on V2
        self._display_power_switch = init_switch(22)  # board pin 15

    @property
    def display_power_led(self) -> LED:
        return self._display_power_led

    @property
    def mqtt_connected_led(self) -> LED:
        return self._mqtt_connected_led

    @property
    def logging_led(self) -> LED:
        return self._logging_led

    @property
    def logging_button(self) -> Switch:
        return self._logging_button

    @property
    def display_power_switch(self) -> Switch:
        return self._display_power_switch


class V3HAL(HardwareAbstractionLayer):
    def __init__(self):
        self._display_power_led = init_led(17)  # board pin 11, green led
        self._mqtt_connected_led = init_led(18)  # board pin 24, yellow led
        self._logging_led = init_led(27)  # board pin 13, red led
        self._logging_button = init_switch(5, PullUpDown.DOWN)  # board pin 29
        self._display_power_switch = init_switch(22)  # board pin 15

    @property
    def display_power_led(self) -> LED:
        return self._display_power_led

    @property
    def mqtt_connected_led(self) -> LED:
        return self._mqtt_connected_led

    @property
    def logging_led(self) -> LED:
        return self._logging_led

    @property
    def logging_button(self) -> Switch:
        return self._logging_button

    @property
    def display_power_switch(self) -> Switch:
        return self._display_power_switch


def get_hal(bike_str: str) -> HardwareAbstractionLayer:
    if bike_str.lower() == "v2":
        return V3HAL()
    elif bike_str.lower() == "v3":
        return V3HAL()
    else:
        raise ValueError(
            f"Unknown bike {bike_str}. Unable to initialise hardware."
        )

