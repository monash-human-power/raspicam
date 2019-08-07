import os
from .overlay import Overlay
from PIL import ImageFont


class OverlayTopStrip(Overlay):
	font_path = os.path.join(os.path.dirname(__file__), 'FreeSans.ttf')
	text_height = 45
	speed_height = 70
	text_font = ImageFont.truetype(font_path, text_height)
	speed_font = ImageFont.truetype(font_path, speed_height)

	data = {
		# das data
		"power": 0,
		"cadence": 0,
		"reed_velocity": 0,
		"gps_speed": 0,
		"reed_distance": 0,
		"count": 0,

		# power model data
		"rec_power": 0,
		"rec_speed": 0,
		"max_speed": 0,
	}

	data_types = {
		# das data
		"power": int,
		"cadence": int,
		"reed_velocity": float,
		"gps_speed": float,
		"reed_distance": float,
		"count": int,

		# power model data
		"rec_power": float,
		"rec_speed": float,
		"max_speed": float,
	}

	def update_overlay(self, data):




if __name__ == '__main__':
	my_overlay = OverlayTopStrip()




