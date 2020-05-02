from abc import ABC, abstractmethod
import time
from typing import Any, List, Optional
import topics as topics


class Data(ABC):
    """ A class to keep track of the most recent bike data for the overlays.

        Data comes into the class in the V2/V3 MQTT formats and may be accessed
        by using this class as a dictionary. This class is implemented by
        versions for specific bikes (DataV2, DataV3,...) """

    data_types = {
        # DAS data
        "power": int,
        "cadence": int,
        "gps": int,
        "gps_speed": float,
        "reed_velocity": float,
        "reed_distance": float,

        # Power model data
        "rec_power": float,
        "rec_speed": float,
        "predicted_max_speed": float,
        "zdist": float,
        "plan_name": str,
    }

    def __init__(self):
        # This is by no means a complete list of data fields we could track -
        # just the ones we currently think we might use on the overlays.
        self.data = {
            # DAS data
            "power": 0,
            "cadence": 0,
            "gps": 0,
            "gps_speed": 0,
            "reed_velocity": 0,
            "reed_distance": 0,

            # Power model data
            "rec_power": 0,
            "rec_speed": 0,
            "predicted_max_speed": 0,
            "zdist": 0,
            "plan_name": "",
        }

        self.message = None
        self.message_received_time = 0
        self.message_duration = 5 # seconds

    def load_message(self, message: str) -> None:
        """ Stores a message which is made available by self.get_message. """
        self.message_received_time = time.time()
        self.message = message

    def has_message(self) -> bool:
        """ Returns true if a message is available for display on the overlay,
            otherwise false.

            Returning false may mean messages have been sent, or the most recent
            message has expired. """
        if not self.message:
            return False
        # Clear the message and return false if enough time has past since
        # the message was received
        if time.time() > self.message_received_time + self.message_duration:
            self.message = None
            return False
        return True

    def get_message(self) -> Optional[str]:
        """ Gets the most recent message from the DAShboard.

            This should only be called if self.has_message returns true. """
        return self.message

    def __getitem__(self, field: str) -> Any:
        """ Gets a the most recent value of a data field.

            This overloads the [] operator e.g. call with data_intance["power"].
            This only allows fetching the data, not assignment. """
        if field in self.data:
            return self.data[field]
        else:
            print(f"WARNING: invalid data field `{field}` used")
            return None

    @abstractmethod
    def load_data(self, topic: str, data: str) -> None:
        """ Updates stored fields with data stored in an MQTT data packet from
            a given topic.

            Only the supplied data fields should be updated, the rest remain as
            they were. This should be implemented by all Data subclasses """
        pass

    @staticmethod
    @abstractmethod
    def get_topics() -> List[str]:
        """ Returns a list of the topics the data for the bike comes from.

            Should be implemented by Data subclasses. """
        pass

    @staticmethod
    def get_data_instance(bike: str) -> "Data":
        """ Returns an instance of Data corresponding to a given bike name """
        if bike == "V2":
            return DataV2()
        if bike == "V3":
            return DataV3()
        raise NotImplementedError(f"Unknown bike: {bike}")


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
        if topic == str(topics.DAShboard.receive_message):
            self.load_message(data)
        elif topic in DataV2.get_topics():
            self.load_query_string(data)

    def load_query_string(self, data: str) -> None:
        """ Updates stored fields with data stored in a V2 query string,
            e.g. `power=200&cadence=95`. """
        terms = data.split("&")
        for term in terms:
            key, value = term.split("=")
            if key not in self.data_types:
                continue
            cast_func = self.data_types[key]
            self.data[key] = cast_func(value)


class DataV3(Data):

    @staticmethod
    def get_topics() -> List[str]:
        return [
            str(topics.DAShboard.receive_message),
        ]

    def load_data(self, topic: str, data: str) -> None:
        """ Updates stored fields with data from a V3 sensor module data
            packet. """
        pass