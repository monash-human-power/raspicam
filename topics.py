"""MQTT Topics for Camera System"""
from enum import Enum, unique
from paho.mqtt.client import topic_matches_sub


@unique
class Topic(Enum):
    """Our base Topic class"""

    def __str__(self):
        return self.value

    def matches(self, other_topic):
        """ Returns true if a topic matches a subscription.
            Accounts for wildcards."""
        return topic_matches_sub(str(self), str(other_topic))


class DAS(Topic):
    """V2 DAS MQTT Topics"""

    data = "data"
    start = "start"
    stop = "stop"


class PowerModel(Topic):
    """Power Model MQTT Topics"""

    plan_name = "power_model/plan_name"
    recommended_sp = "power_model/recommended_SP"
    predicted_max_speed = "power_model/predicted_max_speed"


class PowerModelV3(Topic):
    """Power Model MQTT Topics"""

    plan_name = "power-model/plan-name/filename"
    recommended_sp = "power-model/recommended-sp"
    predicted_max_speed = "power-model/predicted-max-speed"


class Camera(Topic):
    """Camera system MQTT Topics"""

    get_overlays = "camera/get_overlays"
    set_overlay = "camera/set_overlay"
    push_overlays = "camera/push_overlays"
    errors = "/v3/camera/errors"


class DAShboard(Topic):
    """DAShboard MQTT Topics"""

    receive_message = "/v3/camera/primary/message"
    # Note: Wildcard does not include status topics
    recording = "/v3/camera/recording/+"
    recording_start = "/v3/camera/recording/start"
    recording_stop = "/v3/camera/recording/stop"
    recording_status_root = "/v3/camera/recording/status"


class SensorModules(Topic):
    """V3 Wireless sensor module topics"""

    all_sensors = "/v3/wireless-module/+/data"
    front = "/v3/wireless-module/1/data"
    mid = "/v3/wireless-module/2/data"
    back = "/v3/wireless-module/3/data"
    antplus = "/v3/wireless-module/4/data"
