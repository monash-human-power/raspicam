from enum import Enum

class DAS(Enum):
	data = 'data'
	start = 'start'
	stop = 'stop'

class PowerModel(Enum):
	max_speed = 'power_model/max_speed',
	recommended_sp = 'power_model/recommended_SP'

class Camera(Enum):
	get_overlays = 'camera/get_overlays'
	set_overlays = 'camera/set_overlays'
	push_overlays = 'camera/push_overlays'

