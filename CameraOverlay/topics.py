from enum import Enum, unique

@unique
class NeatEnum(Enum):
	def __str__(self):
		return self.value


class DAS(NeatEnum):
	data = 'data'
	start = 'start'
	stop = 'stop'


class PowerModel(NeatEnum):
	plan_name = 'power_model/plan_name'
	max_speed = 'power_model/max_speed'
	recommended_sp = 'power_model/recommended_SP'
	predicted_max_speed = 'power_model/predicted_max_speed'


class Camera(NeatEnum):
	get_overlays = 'camera/get_overlays'
	set_overlays = 'camera/set_overlay'
	push_overlays = 'camera/push_overlays'


if __name__ == '__main__':
	x = PowerModel.max_speed
	print(x)
