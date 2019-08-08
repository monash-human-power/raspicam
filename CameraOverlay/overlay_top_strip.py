import os
from .overlay import Overlay
from PIL import Image, ImageDraw, ImageFont


class OverlayTopStrip(Overlay):

	def __init__(self):
		super(OverlayTopStrip, self).__init__()
		self.font_path = os.path.join(os.path.dirname(__file__), 'FreeSans.ttf')
		self.self.text_height = 45
		self.self.speed_height = 70
		self.self.text_font = ImageFont.truetype(self.font_path, self.self.text_height)
		self.self.speed_font = ImageFont.truetype(self.font_path, self.self.speed_height)


	def on_connect(self, client, userdata, flags, rc):
		print('Connected with rc: {}'.format(rc))
		self.client.subscribe(self.topics)

		# Add static text
		img = Image.new('RGBA', (self.width, self.height))
		draw = ImageDraw.Draw(img)
		draw.text((0, self.text_height * 1), "REC Power:", font=self.text_font, fill='black')
		draw.text((0, self.text_height * 2), "Power:", font=self.text_font, fill='black')
		draw.text((0, self.text_height * 3), "Cadence:", font=self.text_font, fill='black')
		draw.text((0, self.text_height * 4), "Distance:", font=self.text_font, fill='black')
		draw.text((self.width / 2 - 300, self.height - self.speed_height), "SP:", font=self.speed_font, fill='black')
		draw.text((self.width / 2 - 300, self.height - self.speed_height * 2), "REC:", font=self.speed_font, fill='black')
		draw.text((self.width / 2 - 300, self.height - self.speed_height * 3), "MAX:", font=self.speed_font, fill='black')

		overlay = self.add_overlay(img.tobytes(), format='rgba', size=img.size)
		overlay.layer = 3
		overlay.fullscreen = True

	def update_overlay(self, data):
		pass



if __name__ == '__main__':
	my_overlay = OverlayTopStrip()




