from abc import ABC, abstractmethod

from hardware import common
from hardware.led import LED, NopLED, init_led
from hardware.switch import NopSwitch, PullUpDown, Switch, init_switch


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


def cleanup():
    common.cleanup()
