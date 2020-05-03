from json import dumps
import pytest
from time import sleep

from data import Data, DataV2, DataV3
import topics

def test_get_data_instance():
    assert isinstance(Data.get_data_instance("V2"), DataV2)
    assert isinstance(Data.get_data_instance("V3"), DataV3)
    with pytest.raises(NotImplementedError):
        Data.get_data_instance(None)
    with pytest.raises(NotImplementedError):
        Data.get_data_instance("V9000")

def to_query_string(python_dict):
    """ Converts {key1: value1, key2: value2} to key1=value1&key2value2 """
    return "&".join([f"{k}={v}" for k, v in python_dict.items()])

def test_v2_sensor_parsing():
    test_data = {
        "gps": 1,
        "gps_speed": 78.1,
        "reed_velocity": 78.5,
        "reed_distance": 118,
        "power": 320,
        "cadence": 100,
    }

    data = DataV2()
    data.load_data(topics.DAS.data, to_query_string(test_data))

    for key, value in test_data.items():
        assert data[key] == value, f"Key {key} is not being set correctly"

def test_v2_power_model_parsing():
    recommended_sp_data = {
        "rec_power": 500.0,
        "rec_speed": 9.2772,
        "zdist": 1219.0
    }
    max_speed_data = { "predicted_max_speed": 32.911 }
    plan_name_data = { "plan_name": "default.pkl" }

    data = DataV2()
    data.load_data(topics.PowerModel.recommended_sp, to_query_string(recommended_sp_data))
    data.load_data(topics.PowerModel.predicted_max_speed, to_query_string(max_speed_data))
    data.load_data(topics.PowerModel.plan_name, to_query_string(plan_name_data))

    for key, value in { **recommended_sp_data, **max_speed_data, **plan_name_data }.items():
        assert data[key] == value, f"Key {key} is not being set correctly"

def test_v3_messages():
    message_packet = { "message": "testing 123" }
    data = DataV2()
    data.load_data(topics.DAShboard.receive_message, dumps(message_packet))
    assert data.has_message()
    assert data.get_message() == message_packet["message"]
    sleep(data.message_duration)
    assert not data.has_message()

def test_v3_sensor_parsing():
    front_module_data = {
        "sensors": [
            {
                "type": "temperature",
                "value": 24
            },
            {
                "type": "humidity",
                "value": 63
            },
            {
                "type": "steeringAngle",
                "value": 1
            }
        ]
    }
    mid_module_data = {
        "sensors": [
            {
                "type": "co2",
                "value": 34
            },
            {
                "type": "temperature",
                "value": 28
            },
            {
                "type": "humidity",
                "value": 68
            },
            {
                "type": "accelerometer",
                "value": {
                    "x": 1.0,
                    "y": 3.0,
                    "z": -0.5
                }
            },
            {
                "type": "gyroscope",
                "value": {
                    "x": 2.1,
                    "y": 0.2,
                    "z": -0.1
                }
            }
        ]
    }
    back_module_data = {
        "sensors": [
            {
                "type": "co2",
                "value": 35
            },
            {
                "type": "reedVelocity",
                "value": 20.1
            },
            {
                "type": "gps",
                "value": {
                    "speed": 20.5,
                    "satellites": 7,
                    "latitude": 37.8,
                    "longitude": 144.9,
                    "altitude": 95,
                    "course": 23.4
                }
            }
        ]
    }
    das_module_data = {
        "sensors": [
            {
                "type": "power",
                "value": 249
            },
            {
                "type": "cadence",
                "value": 105
            },
            {
                "type": "heartRate",
                "value": 171
            }
        ]
    }

    data = DataV3()
    data.load_data(topics.SensorModules.front, dumps(front_module_data))
    data.load_data(topics.SensorModules.mid, dumps(mid_module_data))
    data.load_data(topics.SensorModules.back, dumps(back_module_data))
    data.load_data(topics.SensorModules.antplus, dumps(das_module_data))

    # No fields tracked from front or mid module
    # Test back module
    assert data["gps"] == 1
    assert data["gps_speed"] == 20.5
    assert data["reed_velocity"] == 20.1
    # Test antplus data
    assert data["power"] == 249
    assert data["cadence"] == 105
    assert data["heartRate"] == 171
