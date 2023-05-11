from abc import ABC, abstractmethod
from json import loads
from time import time
from typing import Any, List, Optional
import config
from mhp import topics


class DataValue:
    """A class to represent a data field (eg. Power, Cadence).

    Attributes:
        value: Any type that represents the current data value of the field
        data_type: Type that represents the attribute of the data
                   (eg. int, str)
        time_updated: Integer that represents the time when value was updated
        DATA_EXPIRY: Constant integer of how long a data value is considered
                     valid for until expired
    """

    def __init__(self, data_type: type, time_to_expire: int = 5) -> None:
        self.value = None
        self.data_type = data_type
        # Time on update is initially set to expire by default
        self.time_updated = 0
        self.time_to_expire = time_to_expire

    def get(self) -> Any:
        """Return the data value if the expiry hasn't exceeded. Otherwise,
        it will return None."""
        if self.is_valid():
            return self.value
        return None

    def get_string(self, decimals: int = 0, scalar: int = 1) -> str:
        """Return the data value in string format, if the expiry hasn't exceeded.
        Otherwise it will return None.

        Args:
            decimals: Integer representing decimal places of the data point
            scalar: Integer used to multiply the data value
        """
        if self.data_type is str:
            return self.get()

        if self.data_type is bool:
            return str(self.get())

        if self.is_valid():
            format_str = f"{{:.{decimals}f}}"
            return format_str.format(self.value * scalar)
        return None

    def update(self, value: Any) -> None:
        """Update the data value and time it was updated.

        Args:
            value: Any type representing the data point of the field
        """
        if type(value) != self.data_type:
            # Casts value when the type is different to the assigned data_type
            value = self.data_type(value)
        self.value = value
        self.time_updated = time()

    def invalidate(self) -> None:
        """Invalidate the data value by making it received a long time ago."""
        self.time_updated = 0

    def is_valid(self) -> bool:
        """Assess whether data is valid by checking if the valid duration
        has exceeded. Return True if current time is less than the time
        when data expires."""
        return time() < self.time_updated + self.time_to_expire


class Data(ABC):
    """A class to keep track of the most recent bike data for the overlays.

    Data comes into the class in the V3 MQTT format and may be accessed
    by using this class as a dictionary. This class is implemented by
    versions for specific bikes (i.e. DataV3)."""

    def __init__(self):
        # This is by no means a complete list of data fields we could track -
        # just the ones we currently think we might use on the overlays.
        self.data = {
            # DAS data
            "power": DataValue(int),
            "cadence": DataValue(int),
            "heartRate": DataValue(int),
            "gps": DataValue(int),
            "gps_speed": DataValue(float),
            "ant_speed": DataValue(float),
            "ant_distance": DataValue(float),
            "reed_velocity": DataValue(float),
            "reed_distance": DataValue(float),
            "wind_speed": DataValue(float),
            "wind_direction": DataValue(float),
            # Power model data
            "rec_power": DataValue(float),
            "rec_speed": DataValue(float),
            "predicted_max_speed": DataValue(float),
            "max_speed_achieved": DataValue(float, time_to_expire=3600),
            "zdist": DataValue(float),
            "plan_name": DataValue(str),
            # Voltage
            "voltage": DataValue(float, config.BATTERY_PUBLISH_INTERVAL),
        }
        self.logging = DataValue(bool, time_to_expire=3600)
        self.message = DataValue(str, 20)

    def set_logging(self, logging: bool) -> None:
        """Set the logging status of the DAS."""
        self.logging.update(logging)

    def is_logging(self) -> bool:
        """Return whether the DAS is logging."""
        return self.logging.get()

    def load_message(self, message: str) -> None:
        """Store a message which is made available by self.get_message."""
        self.message.update(message)

    def has_message(self) -> bool:
        """Check if a message is available for display on the overlay.

        Return True if a message is available for display. Otherwise, return
        false if the message has already been sent of the most recent message
        has expired.
        """
        return self.message.is_valid()

    def get_message(self) -> Optional[str]:
        """Return the most recent message from the DAShboard.

        This should only be called if self.has_message returns true.
        """
        return self.message.get()

    def __getitem__(self, field: str) -> Any:
        """Get the most recent value of a data field.

        This overloads the [] operator e.g. call with data_instance["power"].
        This only allows fetching the data, not assignment.
        """
        if field in self.data:
            return self.data[field]
        else:
            print(f"WARNING: invalid data field `{field}` used")
            return None

    @abstractmethod
    def load_data(self, topic: str, data: str) -> None:
        """Update stored fields with data stored in an MQTT data packet.

        Only the supplied data fields should be updated, the rest remain as
        they were. This should be implemented by all Data subclasses
        """
        pass

    @staticmethod
    @abstractmethod
    def get_topics() -> List[topics.Topic]:
        """Return a list of the topics the data for the bike comes from.

        Should be implemented by Data subclasses."""
        pass


class DataFactory:
    @staticmethod
    def create(bike_version: str) -> Data:
        """Return an instance of Data corresponding to a given bike name."""
        if isinstance(bike_version, str):
            bike_version = bike_version.lower()

        # V2 data is deprecated. Use V3 data format everywhere.
        if bike_version == "v2":
            return DataV3()
        if bike_version == "v3":
            return DataV3()
        raise NotImplementedError(f"Unknown bike: {bike_version}")


class DataV3(Data):
    @staticmethod
    def get_topics() -> List[topics.Topic]:
        # TODO: Not have to read configs everytime
        return [
            topics.WirelessModule.all().start,
            topics.WirelessModule.all().data,
            topics.WirelessModule.all().stop,
            topics.Camera.overlay_message,
            DataV3.create_voltage_topic(),
            topics.BOOST.recommended_sp,
            topics.BOOST.predicted_max_speed,
            topics.BOOST.max_speed_achieved,
            # TODO: Implement handling topics.BOOST.generate_complete
        ]

    @staticmethod
    def create_voltage_topic() -> topics.Topic:
        device = config.read_configs()["device"]
        battery_topic = topics.Camera.status_camera / device / "battery"
        return battery_topic

    def __init__(self):
        super().__init__()
        # Used to detect missed start messages
        self.data_messages_received = 0

    def load_data(self, topic: str, data: str) -> None:
        """Update stored fields with data from a V3 WM data packet."""
        if topic == topics.Camera.overlay_message:
            self.load_message_json(data)
        elif topics.WirelessModule.all().data.matches(topic):
            self.load_sensor_data(data)
            # We have 3 WMs, so in the worst case we shouldn't receive more
            # than four messages due to delay after logging stops. If we do,
            # we know we missed the start message.
            self.data_messages_received += 1
            if not self.logging.get() and self.data_messages_received > 3:
                self.set_logging(True)
        elif topics.WirelessModule.all().start.matches(topic):
            self.data_messages_received = 0
            self.set_logging(True)
        elif topics.WirelessModule.all().stop.matches(topic):
            self.set_logging(False)
        elif self.create_voltage_topic().matches(topic):
            self.load_voltage_data(data)
        elif topic == topics.BOOST.recommended_sp:
            self.load_recommended_sp(data)
        elif topic == topics.BOOST.predicted_max_speed:
            self.load_predicted_max_speed(data)
        elif topic == topics.BOOST.max_speed_achieved:
            self.load_max_speed_achieved(data)

    def load_message_json(self, data: str) -> None:
        """Load a message in the V3 JSON format."""
        message_data = loads(data)
        self.load_message(message_data["message"])

    def load_sensor_data(self, data: str) -> None:
        """Load data in the json V3 wireless sensor module format."""
        module_data = loads(data)
        sensor_data = module_data["sensors"]
        for sensor in sensor_data:
            sensor_name = sensor["type"]
            sensor_value = sensor["value"]

            if sensor_name == "gps":
                self.data["gps"].update(1)
                self.data["gps_speed"].update(sensor_value["speed"] * 3.6)
            elif sensor_name == "antSpeed":
                self.data["ant_speed"].update(sensor_value * 3.6)
            elif sensor_name == "antDistance":
                self.data["ant_distance"].update(sensor_value)
            elif sensor_name == "reedVelocity":
                self.data["reed_velocity"].update(sensor_value * 3.6)
            elif sensor_name == "reedDistance":
                self.data["reed_distance"].update(sensor_value)
            elif sensor_name == "windSpeed":
                print("windSpeed found")
                self.data["wind_speed"].update(sensor_value)
            elif sensor_name == "windDirection":
                # self.data["wind_direction"].update(sensor_value)
                self.data["wind_direction"] = 10
            elif sensor_name in self.data.keys():
                self.data[sensor_name].update(sensor_value)

    def load_voltage_data(self, data: str) -> None:
        voltage_data = loads(data)
        self.data["voltage"].update(voltage_data["voltage"])

    def load_recommended_sp(self, data: str) -> None:
        python_data = loads(data)
        self.data["rec_power"].update(python_data["power"])
        self.data["rec_speed"].update(python_data["speed"] * 3.6)
        self.data["zdist"].update(python_data["zoneDistance"])

    def load_predicted_max_speed(self, data: str) -> None:
        if data == "":
            self.data["predicted_max_speed"].invalidate()
        else:
            python_data = loads(data)
            self.data["predicted_max_speed"].update(python_data["speed"] * 3.6)

    def load_max_speed_achieved(self, data: str) -> None:
        if data == "":
            self.data["max_speed_achieved"].invalidate()
        else:
            python_data = loads(data)
            self.data["max_speed_achieved"].update(python_data["speed"] * 3.6)
