import os
from .overlay import Overlay
from PIL import ImageFont


class OverlayTopStrip(Overlay):
	font_path = os.path.join(os.path.dirname(__file__), 'FreeSans.ttf')
	text_height = 45
	speed_height = 70
	text_font = ImageFont.truetype(font_path, text_height)
	speed_font = ImageFont.truetype(font_path, speed_height)



	def update_overlay(self, data):
		pass



if __name__ == '__main__':
	my_overlay = OverlayTopStrip()




