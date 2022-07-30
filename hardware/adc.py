from abc import ABC, abstractmethod

from hardware.common import ON_PI

if ON_PI:
    import adafruit_mcp3xxx.mcp3004
    import board
    import busio
    import digitalio
    from adafruit_mcp3xxx.analog_in import AnalogIn


class ADC(ABC):
    @abstractmethod
    def read_voltage(self) -> float:
        pass


class MCP3004(ADC):
    def __init__(self, spi, cs, calibration_factor=1.0):
        mcp = mcp3004.MCP3004(spi, cs)
        self.adc = AnalogIn(mcp, mcp3004.P0)

        self.calibration_factor = calibration_factor

    def read_voltage(self) -> float:
        return self.adc.voltage * self.calibration_factor


class DummyADC(ADC):
    def __init__(self, voltage: float):
        self.voltage = voltage

    def read_voltage(self) -> float:
        return self.voltage


def init_v3_battery_adc() -> ADC:

    if not ON_PI:
        return DummyADC(3.7)

    # See https://github.com/monash-human-power/V3-display-unit-pcb-tests/blob/72d02c270be413b1d4e97b9d10a33c97f551eafe/calibrate.py # noqa: E501
    battery_calibration_factor = 3.1432999689025483

    # ADC is connected to SPI bus 0, CE pin 0
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.CE0)
    return MCP3004(spi, cs, battery_calibration_factor)
