import os
import time
from overlay import Overlay
from PIL import Image, ImageDraw, ImageFont
import topics


class OverlayAllStats(Overlay):

	def __init__(self):
		super(OverlayAllStats, self).__init__()
	
		self.prev_time = 0
		
		self.font_path = os.path.join(os.path.dirname(__file__), 'FreeSans.ttf')
		self.bottom_text_height = 70
		self.bottom_text_font = ImageFont.truetype(self.font_path, self.bottom_text_height)
		self.top_text_height = 45
		self.top_text_font = ImageFont.truetype(self.font_path, self.top_text_height)
		self.top_box_height = 80
		self.top_box_width = self.width
		

	def on_connect(self, client, userdata, flags, rc):
		print("Connected with rc: " + str(rc))
		# Subscribed topics
		client.subscribe("start")
		client.subscribe("data")
		client.subscribe("stop")
		client.subscribe("power_model/recommended_SP")
		client.subscribe("power_model/predicted_max_speed")
		client.subscribe("power_model/plan_name")

		# Add static text
		img = Image.new('RGBA', (self.width, self.height))
		draw = ImageDraw.Draw(img)
		draw.rectangle(((0, 0), (self.top_box_width, self.top_box_height)), fill='black')
		draw.text((0, (self.top_box_height - self.top_text_height) / 2 + 8), 'T: ', font=self.top_text_font, fill='white')
		draw.text((256, (self.top_box_height - self.top_text_height) / 2 + 8), 'ZDL: ', font=self.top_text_font, fill='white')
		draw.text((512, (self.top_box_height - self.top_text_height) / 2 + 8), 'RP: ', font=self.top_text_font, fill='white')
		draw.text((768, (self.top_box_height - self.top_text_height) / 2 + 8), 'PMV: ', font=self.top_text_font, fill='white')
		draw.text((1024, (self.top_box_height - self.top_text_height) / 2 + 8), 'MS: ', font=self.top_text_font, fill='white')
		overlay = self.camera.add_overlay(img.tobytes(), format='rgba', size=img.size)
		overlay.layer = 3
		overlay.fullscreen = False
		overlay.window = (0, -20, self.width, self.height)

	def on_message(self, client, userdata, msg):
		print(msg.topic + " " + str(msg.payload.decode("utf-8")))
		current_time = round(time.time(), 2)
		if msg.topic == "power_model/recommended_SP":
			req_data = str(msg.payload.decode("utf-8"))
			parsed_data = self.parse_data(req_data)
			self.data["rec_power"] = int(parsed_data["rec_power"])
			self.data["zdist"] = int(parsed_data["zdist"])
		elif msg.topic == "power_model/predicted_max_speed":
			pred_max_speed = str(msg.payload.decode("utf-8"))
			parsed_data = self.parse_data(pred_max_speed)
			self.data["pred_max_speed"] = int(parsed_data["predicted_max_speed"])
		elif msg.topic == "power_model/plan_name":
			plan_name = str(msg.payload.decode("utf-8"))
			parsed_data = self.parse_data(plan_name)
			self.data["plan_name"] = str(parsed_data["plan_name"])
		elif msg.topic == "data":
			data = str(msg.payload.decode("utf-8"))
			parsed_data = self.parse_data(data)
			print(str(parsed_data))
			self.data["power"] += int(parsed_data["power"])
			self.data["cadence"] += int(parsed_data["cadence"])
			if int(parsed_data["gps"]) == 1:
				self.data["gps_speed"] += float(parsed_data["gps_speed"])
			self.data["reed_distance"] += float(parsed_data["reed_distance"])
			self.data["count"] = self.data["count"] + 1
			if self.prev_time == 0:
				total_time = current_time - self.start_time
			else:
				total_time = current_time - self.prev_time
			update_time = 1
			if total_time >= update_time:
				self.prev_time = current_time
				# Create a transparent image to attach text
				img = Image.new('RGBA', (self.width, self.height))
				draw = ImageDraw.Draw(img)

				# Display elapsed time:
				hours, rem = divmod(time.time() - self.start_time, 3600)
				minutes, seconds = divmod(rem, 60)
				draw.text((50, (self.top_box_height - self.top_text_height) / 2 + 8),
				          "{:0>2}:{:0>2}".format(int(minutes), int(seconds)), font=self.top_text_font, fill='white')

				# Display power
				if self.data["power"] != 0:
					power = self.data["power"] / self.data["count"]
					rec_power = self.data["rec_power"]
					# Display recommended power
					draw.text((600, (self.top_box_height - self.top_text_height) / 2 + 8), "{0}".format(round(rec_power, 0)),
					          font=self.top_text_font, fill='white')
					# Display power (no colour change)
					draw.text((self.width / 2 - 90, self.height - self.bottom_text_height), "P:{0}".format(round(power, 2)),
					          font=self.bottom_text_font, fill='red')

				# Display speed
				if int(parsed_data["gps"]) == 1:
					if self.data["gps_speed"] != 0:
						# Predicted max speed
						pred_max_speed = self.data["pred_max_speed"]
						draw.text((890, (self.top_box_height - self.top_text_height) / 2 + 8),
						          "{0}".format(round(pred_max_speed, 2)), font=self.top_text_font, fill='white')

						# Actual speed (no colour change)
						speed = self.data["gps_speed"] / self.data["count"]
						speed_text = "{0}".format(round(speed, 2))
						draw.text((self.width / 2 - 90, self.height - self.bottom_text_height * 2 - 30),
						          "S:{0}".format(round(speed, 2)), font=self.bottom_text_font, fill='red')

						# Actual max speed
						self.actual_max(speed)
						draw.text((1120, (self.top_box_height - self.top_text_height) / 2 + 8), "{0}".format(int(self.max_speed)),
						          font=self.top_text_font, fill='white')

				# Display zone distance left (bugged)
				if self.data["zdist"] != 0:
					zdist_left = self.data["zdist"]
					draw.text((360, (self.top_box_height - self.top_text_height) / 2 + 8), "{0}".format(int(zdist_left)),
					          font=self.top_text_font, fill='white')

				# Display plan name and clear after 15 secs
				if self.data["plan_name"] != '' and time.time() - self.start_time <= 15:
					plan_name = self.data["plan_name"]
					draw.text((0, self.height - self.top_text_height), "{}".format(plan_name), font=self.top_text_font, fill='red')

				# Remove and add the image to the preview overlay
				if self.prev_overlay:
					self.camera.remove_overlay(self.prev_overlay)
				overlay = self.camera.add_overlay(img.tobytes(), format='rgba', size=img.size)
				overlay.layer = 3
				overlay.fullscreen = False
				overlay.window = (0, -20, self.width, self.height)
				self.prev_overlay = overlay

				# Reset variables
				self.data["power"] = 0
				self.data["cadence"] = 0
				self.data["gps_speed"] = 0
				self.data["reed_distance"] = 0
				self.data["count"] = 0
				
				
			


if __name__ == '__main__':
	my_overlay = OverlayAllStats()
	my_overlay.connect()
