from PIL import Image, ImageDraw, ImageFont


def main():
	# Resolution of camera preview
	WIDTH = 1280
	HEIGHT = 740

	bottom_text_height = 70
	bottom_text_font = ImageFont.truetype('/Users/harsilpatel/Coding/MHP_Raspicam/CameraOverlay/LibreCaslonText-Regular.ttf', bottom_text_height)
	top_text_height = 45
	top_text_font = ImageFont.truetype('/Users/harsilpatel/Coding/MHP_Raspicam/CameraOverlay/LibreCaslonText-Regular.ttf', top_text_height)
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


if __name__ == '__main__':
	main()
