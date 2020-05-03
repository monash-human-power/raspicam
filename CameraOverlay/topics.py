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
    """DAS MQTT Topics"""
    data = 'data'
    start = 'start'
    stop = 'stop'

class PowerModel(Topic):
    """Power Model MQTT Topics"""
    plan_name = 'power_model/plan_name'
    max_speed = 'power_model/max_speed'
    recommended_sp = 'power_model/recommended_SP'
    predicted_max_speed = 'power_model/predicted_max_speed'

class Camera(Topic):
    """Camera system MQTT Topics"""
    get_overlays = 'camera/get_overlays'
    set_overlays = 'camera/set_overlay'
    push_overlays = 'camera/push_overlays'

class DAShboard(Topic):
    """DAShboard MQTT Topics"""
    receive_message = '/v3/camera/primary/message'

class SensorModule(Topic):
    """V3 Wireless sensor module topics"""
    data = "/v3/wireless-module/+/data"