from typing import Any
import CameraOverlay.topics as topics

V2_DATA_TOPICS = [
    str(topics.DAS.data),
    str(topics.PowerModel.recommended_sp),
    str(topics.PowerModel.predicted_max_speed),
    str(topics.PowerModel.plan_name),
]

class Data:

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
        self._has_new_data = False

    def load_v2_query_string(self, data: str) -> None:
        terms = data.split("&")
        for term in terms:
            key, value = term.split("=")
            if key not in self.data_types:
                continue
            cast_func = self.data_types[key]
            self.data[key] = cast_func(value)
        self._has_new_data = True

    def load_v3_module_data(self, data: str) -> None:
        pass

    def has_new_data(self) -> bool:
        if self._has_new_data:
            self._has_new_data = False
            return True
        return False

    # Overload the [] operator
    def __getitem__(self, key: str) -> Any:
        if key in self.data:
            return self.data[key]
        else:
            print(f"WARNING: invalid data key `{key}` used")
