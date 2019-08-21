import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1280
HEIGHT = 740
FONT = os.path.join(os.path.dirname(__file__), 'LibreCaslonText-Regular.ttf')


def overlay_two():
	bottom_text_height = 70
	# _ = ImageFont.truetype(FONT, bottom_text_height)
	top_text_height = 45
	top_text_font = ImageFont.truetype(FONT, top_text_height)
	top_box_height = 80
	top_box_width = WIDTH

	img = Image.new('RGBA', (WIDTH, HEIGHT))
	draw = ImageDraw.Draw(img)
	draw.rectangle(((0, 0), (top_box_width, top_box_height)), fill='black')
	draw.text((0, (top_box_height - top_text_height) / 2 + 8), 'T: ', font=top_text_font, fill='white')
	draw.text((256, (top_box_height - top_text_height) / 2 + 8), 'ZDL: ', font=top_text_font, fill='white')
	draw.text((512, (top_box_height - top_text_height) / 2 + 8), 'RP: ', font=top_text_font, fill='white')
	draw.text((768, (top_box_height - top_text_height) / 2 + 8), 'PMV: ', font=top_text_font, fill='white')
	draw.text((1024, (top_box_height - top_text_height) / 2 + 8), 'MS: ', font=top_text_font, fill='white')
	# overlay = camera.add_overlay(img.tobytes(), format='rgba', size=img.size)
	# overlay.layer = 3
	# overlay.fullscreen = False
	# overlay.window = (0, -20, WIDTH, HEIGHT)
	img.show()


def overlay_one():
	speed_height = 70
	speed_font = ImageFont.truetype(FONT, speed_height)
	text_height = 45
	text_font = ImageFont.truetype(FONT, text_height)

	img = Image.new('RGBA', (WIDTH, HEIGHT))
	draw = ImageDraw.Draw(img)
	draw.text((0, text_height * 1), "REC Power:", font=text_font, fill='black')
	draw.text((0, text_height * 2), "Power:", font=text_font, fill='black')
	draw.text((0, text_height * 3), "Cadence:", font=text_font, fill='black')
	draw.text((0, text_height * 4), "Distance:", font=text_font, fill='black')
	draw.text((WIDTH / 2 - 300, HEIGHT - speed_height), "SP:", font=speed_font, fill='black')
	draw.text((WIDTH / 2 - 300, HEIGHT - speed_height * 2), "REC:", font=speed_font, fill='black')
	draw.text((WIDTH / 2 - 300, HEIGHT - speed_height * 3), "MAX:", font=speed_font, fill='black')
	img.show()


if __name__ == '__main__':
	overlay_one()
	overlay_two()
