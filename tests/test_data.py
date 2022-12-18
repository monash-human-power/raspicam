from json import dumps
import pytest
from time import sleep

from data import DataValue, DataFactory, DataV3
from mhp import topics


class TestDataValue:
    @staticmethod
    def test_instance_creation():
        data_value = DataValue(str)

        assert data_value.data_type == str, "Type is not set properly"
        assert (
            data_value.time_to_expire == 5
        ), "Default time is not set to 5 seconds"
        assert not data_value.is_valid(), "Data is not invalid by default"

    @staticmethod
    def test_data_update():
        data_value = DataValue(int)
        data_value.update(100)

        assert data_value.value == 100, "Data is not updated properly"
        assert (
            data_value.is_valid()
        ), "When data is updated, it should be ruled valid"
        sleep(data_value.time_to_expire)
        assert (
            not data_value.is_valid()
        ), "After 5 seconds passes, data should be ruled invalid"

    @staticmethod
    def test_data_get():
        data_value = DataValue(float)
        data_value.update(26)

        assert data_value.get() == 26, "Data was not returned properly."
        assert (
            data_value.get_string() == "26"
        ), "Data as a string was not returned properly"
        assert (
            data_value.get_string(1) == "26.0"
        ), "Data as a string was not returned with the correct decimal places"


class TestDataFactory:
    @staticmethod
    def test_instance_creation():
        assert isinstance(DataFactory.create("v2"), DataV3)
        assert isinstance(DataFactory.create("V3"), DataV3)

    @staticmethod
    def test_invalid_bike_names():
        with pytest.raises(NotImplementedError):
            DataFactory.create(None)
        with pytest.raises(NotImplementedError):
            DataFactory.create("V9000")


class TestDataV3:
    @staticmethod
    def test_v3_messages():
        message_packet = {"message": "testing 123"}
        data = DataV3()
        data.load_data(topics.Camera.overlay_message, dumps(message_packet))
        assert data.has_message()
        assert data.get_message() == message_packet["message"]
        sleep(data.message.time_to_expire)
        assert not data.has_message()

    @staticmethod
    def test_v3_sensor_parsing():
        front_module_data = {
            "sensors": [
                {"type": "temperature", "value": 24},
                {"type": "humidity", "value": 63},
                {"type": "steeringAngle", "value": 1},
            ]
        }
        mid_module_data = {
            "sensors": [
                {"type": "co2", "value": 34},
                {"type": "temperature", "value": 28},
                {"type": "humidity", "value": 68},
                {
                    "type": "accelerometer",
                    "value": {"x": 1.0, "y": 3.0, "z": -0.5},
                },
                {
                    "type": "gyroscope",
                    "value": {"x": 2.1, "y": 0.2, "z": -0.1},
                },
            ]
        }
        back_module_data = {
            "sensors": [
                {"type": "co2", "value": 35},
                {"type": "reedVelocity", "value": 20.1},
                {"type": "reedDistance", "value": 1040.3},
                {
                    "type": "gps",
                    "value": {
                        "speed": 20.5,
                        "satellites": 7,
                        "latitude": 37.8,
                        "longitude": 144.9,
                        "altitude": 95,
                        "course": 23.4,
                    },
                },
            ]
        }
        das_module_data = {
            "sensors": [
                {"type": "power", "value": 249},
                {"type": "cadence", "value": 105},
                {"type": "heartRate", "value": 171},
            ]
        }

        data = DataV3()
        data.load_data(
            topics.WirelessModule.id(1).data, dumps(front_module_data)
        )
        data.load_data(
            topics.WirelessModule.id(2).data, dumps(mid_module_data)
        )
        data.load_data(
            topics.WirelessModule.id(3).data, dumps(back_module_data)
        )
        data.load_data(
            topics.WirelessModule.id(4).data, dumps(das_module_data)
        )

        # No fields tracked from front or mid module
        # Test back module
        assert data["gps"].get() == 1
        assert data["gps_speed"].get() == 20.5 * 3.6
        assert data["reed_velocity"].get() == 20.1 * 3.6
        assert data["reed_distance"].get() == 1040.3
        # Test antplus data
        assert data["power"].get() == 249
        assert data["cadence"].get() == 105
        assert data["heartRate"].get() == 171

    @staticmethod
    def test_v3_power_model_parsing():
        recommended_sp_data = {
            "power": 10,
            "speed": 20,
            "zoneDistance": 30,
            "distanceOffset": 40,
            "distanceLeft": 50,
        }
        max_speed_data = {"speed": 100}

        data = DataV3()
        data.load_data(topics.BOOST.recommended_sp, dumps(recommended_sp_data))
        data.load_data(topics.BOOST.predicted_max_speed, dumps(max_speed_data))

        assert data["rec_power"].get() == 10
        assert data["rec_speed"].get() == 20 * 3.6
        assert data["zdist"].get() == 30
        assert data["predicted_max_speed"].get() == 100 * 3.6
