from abc import ABC, abstractmethod
from json import loads
from time import time
from datetime import datetime
from typing import Any, List, Optional

import topics


class DataField:
    """ A class to represent a data field (eg. Power, Cadence).

    Attributes:

        value: Any type that represents the current data value of the field
        data_type: Type that represents the attribute of the data (eg. int, str)
        time_updated: Integer that represents the time when value was updated
        DATA_EXPIRY: Constant integer of how long a data value is considered 
                     valid for until expired
    """

    DATA_EXPIRY = 5
    
    def __init__(self, data_type: type) -> None:
        self.value = None
        self.data_type = data_type
        # Time on update is initially set to expire by default
        self.time_updated = 0

    def get(self) -> Any:
        """ Return the data value if the expiry hasn't exceeded. Otherwise,
            it will return None. """
        if self.is_valid():
            return self.value
        return None

    def get_string(self, decimals = 0, scalar = 1) -> str:
        """ Return the data value in string format, if the expiry hasn't exceeded.
            Otherwise it will return None. """
        if self.data_type is str:
            return self.get()

        if self.is_valid():
            format_str = f"{{:.{decimals}f}}"
            return format_str.format(self.value * scalar)
        return None
    
    def update(self, value: Any) -> None:
        """ Update the data value and time it was updated. """
        self.value = value
        self.time_updated = time()
    
    def is_valid(self) -> bool:
        """ Assess whether data is still valid by checking if the valid duration
            has exceeded. 
            
            Return True if current time is less than the time when data expires.
            """
        return time() < self.time_updated + DataField.DATA_EXPIRY


class Data(ABC):
    """ A class to keep track of the most recent bike data for the overlays.

        Data comes into the class in the V2/V3 MQTT formats and may be accessed
        by using this class as a dictionary. This class is implemented by
        versions for specific bikes (DataV2, DataV3,...) """

    def __init__(self):
        # This is by no means a complete list of data fields we could track -
        # just the ones we currently think we might use on the overlays.
        self.data = {
            # DAS data
            "power": DataField(int),
            "cadence": DataField(int),
            "heartRate": DataField(int),
            "gps": DataField(int),
            "gps_speed": DataField(float),
            "reed_velocity": DataField(float),
            "reed_distance": DataField(float),
            # Power model data
            "rec_power": DataField(float),
            "rec_speed": DataField(float),
            "predicted_max_speed": DataField(float),
            "zdist": DataField(float),
            "plan_name": DataField(str),
        }

        self.message = None
        self.message_received_time = 0
        self.message_duration = 5  # seconds

    def load_message(self, message: str) -> None:
        """Store a message which is made available by self.get_message."""
        self.message_received_time = time()
        self.message = message

    def has_message(self) -> bool:
        """Check if a message is available for display on the overlay.

        Should return true if the message is available for display.

        Returning false may mean messages have been sent, or the most
        recent message has expired.
        """
        if not self.message:
            return False
        # Clear the message and return false if enough time has past since
        # the message was received
        if time() > self.message_received_time + self.message_duration:
            self.message = None
            return False
        return True

    def get_message(self) -> Optional[str]:
        """Get the most recent message from the DAShboard.

        This should only be called if self.has_message returns true.
        """
        return self.message

    def __getitem__(self, field: str) -> Any:
        """Get the most recent value of a data field.

        This overloads the [] operator e.g. call with data_intance["power"].
        This only allows fetching the data, not assignment.
        """
        if field in self.data:
            return self.data[field] # TODO
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
    def get_topics() -> List[str]:
        """ Return a list of the topics the data for the bike comes from.

            Should be implemented by Data subclasses. """
        pass


class DataFactory:
    @staticmethod
    def create(bike_version: str) -> Data:
        """Return an instance of Data corresponding to a given bike name."""
        if isinstance(bike_version, str):
            bike_version = bike_version.lower()

        if bike_version == "v2":
            return DataV2()
        if bike_version == "v3":
            return DataV3()
        raise NotImplementedError(f"Unknown bike: {bike_version}")


class DataV2(Data):
    @staticmethod
    def get_topics() -> List[str]:
        return [
            str(topics.DAS.data),
            str(topics.PowerModel.recommended_sp),
            str(topics.PowerModel.predicted_max_speed),
            str(topics.PowerModel.plan_name),
            str(topics.DAShboard.receive_message),
        ]

    def load_data(self, topic: str, data: str) -> None:
        """ Loads V2 query strings and V3 DAShboard messages """
        if topics.DAShboard.receive_message.matches(topic):
            self.load_message(data)
        elif str(topic) in DataV2.get_topics():
            self.load_query_string(data)

    def load_query_string(self, data: str) -> None:
        """Update stored fields with data stored in a V2 query string.

        Example:
            `power=200&cadence=95`

        """
        terms = data.split("&")
        for term in terms:
            key, value = term.split("=")
            if key not in self.data:
                continue
            cast_func = self.data[key].data_type
            self.data[key].update(cast_func(value))


class DataV3(Data):
    @staticmethod
    def get_topics() -> List[str]:
        return [
            str(topics.SensorModules.all_sensors),
            str(topics.DAShboard.receive_message),
            str(topics.PowerModelV3.recommended_sp),
            str(topics.PowerModelV3.predicted_max_speed),
            str(topics.PowerModelV3.plan_name),
        ]

    def load_data(self, topic: str, data: str) -> None:
        """Update stored fields with data from a V3 sensor module data packet.
        """
        if topics.DAShboard.receive_message.matches(topic):
            self.load_message_json(data)
        elif topics.SensorModules.all_sensors.matches(topic):
            self.load_sensor_data(data)
        elif topics.PowerModelV3.recommended_sp.matches(topic):
            self.load_recommended_sp(data)
        elif topics.PowerModelV3.predicted_max_speed.matches(topic):
            self.load_predicted_max_speed(data)
        elif topics.PowerModelV3.plan_name.matches(topic):
            self.load_plan_name(data)

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
                self.data["gps_speed"].update(float(sensor_value["speed"]))
            elif sensor_name == "reedVelocity":
                self.data["reed_velocity"].update(float(sensor_value))
            elif sensor_name in self.data_types:
                cast_func = self.data[sensor_name].data_type
                self.data[sensor_name].update(cast_func(sensor_value))

    def load_recommended_sp(self, data: str) -> None:
        python_data = loads(data)
        self.data["rec_power"].update(python_data["power"])
        self.data["rec_speed"].update(python_data["speed"])
        self.data["zdist"].update(python_data["zoneDistance"])

    def load_predicted_max_speed(self, data: str) -> None:
        python_data = loads(data)
        self.data["predicted_max_speed"].update(python_data["speed"])

    def load_plan_name(self, data: str) -> None:
        python_data = loads(data)
        self.data["plan_name"].update(python_data["filename"])
