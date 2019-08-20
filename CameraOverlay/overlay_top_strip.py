import os
import time
from overlay import Overlay
from PIL import Image, ImageDraw, ImageFont
import topics


class OverlayTopStrip(Overlay):

	def __init__(self):
		super(OverlayTopStrip, self).__init__()
		self.font_path = os.path.join(os.path.dirname(__file__), 'FreeSans.ttf')
		self.text_height = 45
		self.speed_height = 70
		self.text_font = ImageFont.truetype(self.font_path, self.text_height)
		self.speed_font = ImageFont.truetype(self.font_path, self.speed_height)

	def on_connect(self, client, userdata, flags, rc):
		print('Connected with rc: {}'.format(rc))
		# self.client.subscribe(self.topics)
		client.subscribe(topics.DAS.start)
		client.subscribe(topics.DAS.data)
		client.subscribe(topics.DAS.stop)
		client.subscribe(topics.PowerModel.recommended_sp)
		client.subscribe(topics.PowerModel.max_speeds)

		# Add static text
		img = Image.new('RGBA', (self.width, self.height))
		draw = ImageDraw.Draw(img)
		draw.text((0, self.text_height * 1), "REC Power:", font=self.text_font, fill='black')
		draw.text((0, self.text_height * 2), "Power:", font=self.text_font, fill='black')
		draw.text((0, self.text_height * 3), "Cadence:", font=self.text_font, fill='black')
		draw.text((0, self.text_height * 4), "Distance:", font=self.text_font, fill='black')
		draw.text((self.width / 2 - 300, self.height - self.speed_height), "SP:", font=self.speed_font, fill='black')
		draw.text((self.width / 2 - 300, self.height - self.speed_height * 2), "REC:", font=self.speed_font,
		          fill='black')
		draw.text((self.width / 2 - 300, self.height - self.speed_height * 3), "MAX:", font=self.speed_font,
		          fill='black')

		overlay = self.camera.add_overlay(img.tobytes(), format='rgba', size=img.size)
		overlay.layer = 3
		overlay.fullscreen = True

	def on_message(self, client, userdata, msg):
		topic = msg.topic
		print(topic + " " + str(msg.payload.decode("utf-8")))
		current_time = round(time.time(), 2)

		if topic == topics.PowerModel.recommended_sp:
			req_data = str(msg.payload.decode("utf-8"))
			parsed_data = self.parse_data(req_data)
			self.data["rec_power"] = float(parsed_data["rec_power"])
			self.data["rec_speed"] = float(parsed_data["rec_speed"])
		elif topic == topics.PowerModel.max_speed:
			max_speed = str(msg.payload.decode("utf-8"))
			self.data["max_speed"] = float(max_speed)
		elif topic == topics.DAS.data:
			data = str(msg.payload.decode("utf-8"))
			parsed_data = self.parse_data(data)
			print(str(parsed_data))
			self.data["power"] += int(parsed_data["power"])
			self.data["cadence"] += int(parsed_data["cadence"])
			if int(parsed_data["gps"]) == 1:
				self.data["gps_speed"] += float(parsed_data["gps_speed"])
			self.data["reed_distance"] += float(parsed_data["reed_distance"])
			self.data["reed_velocity"] += float(parsed_data["reed_velocity"])
			self.data["count"] = self.data["count"] + 1
			total_time = current_time - self.start_time
			update_time = 0.5
			if total_time >= update_time:
				self.start_time = current_time
				# Create a transparent image to attach text
				img = Image.new('RGBA', (self.width, self.height))
				draw = ImageDraw.Draw(img)

				# Display power
				if self.data["power"] != 0:
					power = self.data["power"] / self.data["count"]
					rec_power = self.data["rec_power"]
					tolerance = 0.05
					# Display recommended power
					draw.text((300, self.text_height * 1), "{0}".format(round(rec_power, 2)), font=self.text_font,
					          fill='black')
					# Display power
					if power > rec_power and power < (rec_power + (rec_power * tolerance)):
						draw.text((300, self.text_height * 2), "{0}".format(round(power, 2)), font=self.text_font,
						          fill='green')

					elif power > (rec_power + (rec_power * tolerance)):
						draw.text((300, self.text_height * 2), "{0}".format(round(power, 2)), font=self.text_font,
						          fill='red')

					else:
						draw.text((300, self.text_height * 2), "{0}".format(round(power, 2)), font=self.text_font,
						          fill='black')

				# Display cadence
				if self.data["cadence"] != 0:
					cadence = self.data["cadence"] / self.data["count"]
					draw.text((300, self.text_height * 3), "{0}".format(round(cadence, 2)), font=self.text_font,
					          fill='black')

				# Display speed
				if self.data["reed_velocity"] != 0:
					speed_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',
					                                self.speed_height)
					# Max Speed
					max_speed = self.data["max_speed"]
					max_speed_text = "{0} km/h".format(round(max_speed, 2))
					draw.text((self.width / 2 - 70, self.height - self.speed_height * 3), max_speed_text,
					          font=speed_font,
					          fill='black')

					# Recommended speed
					rec_speed = self.data["rec_speed"]
					rec_speed_text = "{0} km/h".format(round(rec_speed, 2))
					draw.text((self.width / 2 - 70, self.height - self.speed_height * 2), rec_speed_text,
					          font=speed_font,
					          fill='black')

					# Actual speed
					speed = self.data["reed_velocity"] / self.data["count"]
					speed_text = "{0} km/h".format(round(speed, 2))
					if speed > rec_speed and speed < (rec_speed + (rec_speed * tolerance)):
						draw.text((self.width / 2 - 70, self.height - self.speed_height), speed_text, font=speed_font,
						          fill='green')

					elif speed > (rec_speed + (rec_speed * tolerance)):
						draw.text((self.width / 2 - 70, self.height - self.speed_height), speed_text, font=speed_font,
						          fill='red')

					else:
						draw.text((self.width / 2 - 70, self.height - self.speed_height), speed_text, font=speed_font,
						          fill='black')

				# Display reed_distance (distance travelled)
				if self.data["reed_distance"] != 0:
					reed_distance = self.data["reed_distance"] / self.data["count"]
					draw.text((300, self.text_height * 4), "{0}".format(round(reed_distance, 2)), font=self.text_font,
					          fill='black')

				# Remove and add the image to the preview overlay
				if self.prev_overlay:
					self.camera.remove_overlay(self.prev_overlay)
				overlay = self.camera.add_overlay(img.tobytes(), format='rgba', size=img.size)
				overlay.layer = 3
				overlay.fullscreen = True
				self.prev_overlay = overlay

				# Reset variables
				# self.reset_variables()

				# Reset variables
				self.data["power"] = 0
				self.data["cadence"] = 0
				self.data["gps_speed"] = 0
				self.data["reed_velocity"] = 0
				self.data["reed_distance"] = 0
				self.data["count"] = 0


if __name__ == '__main__':
	my_overlay = OverlayTopStrip()
	my_overlay.connect()
