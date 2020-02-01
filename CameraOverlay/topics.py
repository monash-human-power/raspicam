"""MQTT Topics for Camera System"""
from enum import Enum, unique

@unique
class NeatEnum(Enum):
    """Our base Enum class"""
    def __str__(self):
        return self.value

class DAS(NeatEnum):
    """DAS MQTT Topics"""
    data = 'data'
    start = 'start'
    stop = 'stop'

class PowerModel(NeatEnum):
    """Power Model MQTT Topics"""
    plan_name = 'power_model/plan_name'
    max_speed = 'power_model/max_speed'
    recommended_sp = 'power_model/recommended_SP'
    predicted_max_speed = 'power_model/predicted_max_speed'

class Camera(NeatEnum):
    """Camera system MQTT Topics"""
    get_overlays = 'camera/get_overlays'
    set_overlays = 'camera/set_overlay'
    push_overlays = 'camera/push_overlays'

class DAShboard(NeatEnum):
        """DAShboard MQTT Topics"""
        receive_message = '/v3/camera/primary/message'