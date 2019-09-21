"""MQTT Topics for Camera System"""
from enum import Enum, unique


@unique
class NeatEnum(Enum):
	"""Our base Enum class"""

	def __str__(self):
		return self.value


class DAS(NeatEnum):
	"""DAS MQTT Topics"""
	start = 'start'  # Sent when switch for DAS is switched off
	stop = 'stop'  # Sent when data comes through via serial from the Teensy
	data = 'data'  # Sent when switch for DAS is switched on
	filename = 'filename'  # Receive filename from server


class PowerModel(NeatEnum):
	"""Power Model MQTT Topics"""
	start = 'power_model/start'  # Start power model
	stop = 'power_model/stop'
	generate_power_plan = 'power_model/generate_power_plan'  # From power-zone.htm
	calibrate = 'power_model/calibrate'  # Calibrate current distance for power model
	calibrate_reset = 'power_model/calibrate/reset'  # Button to reset calibrated distance.
	plan_generated = 'power_model/plan_generated'  # Gets success message
	plan_name = 'power_model/plan_name'  # Shows what plan is loaded
	max_speed = 'power_model/max_speed'  # Maximum theoretical speed
	zone_confirmation = 'power_model/zone_confirmation'  # Gets list of zone distances to confirm right plan

	recommended_sp = 'power_model/recommended_SP'  # Recommended speed and power and zone distance and distance left
	predicted_max_speed = 'power_model/predicted_max_speed'  # Maximum theoretical speed


class Camera(NeatEnum):
	"""Camera system MQTT Topics"""
	get_overlays = 'camera/get_overlays'  # Gets the list of overlays on the cameras
	set_overlay = 'camera/set_overlay'  # Method to set the overlays
	push_overlays = 'camera/push_overlays'  # To push the overlays to the server
