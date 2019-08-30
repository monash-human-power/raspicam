import time
from overlay import Overlay, Color
import topics


class OverlayAllStats(Overlay):

	topics = [
			topics.DAS.start,
			topics.DAS.data,
			topics.DAS.stop,
			topics.PowerModel.recommended_sp,
			topics.PowerModel.max_speed,
			topics.PowerModel.plan_name,
	]

	def __init__(self):
		super(OverlayAllStats, self).__init__()

		self.prev_time = 0

		self.bottom_text_height = 70
		self.bottom_text_pos_x = self.width // 2 - 150
		self.bottom_text_pos_y = self.height - 8
		self.bottom_text_size = 2.2
		self.top_box_height = 60
		self.top_box_width = self.width
		self.top_text_pos = self.top_box_height - 15

	def on_connect(self, client, userdata, flags, rc):
		print("Connected with rc: " + str(rc))
		for topic in OverlayAllStats.topics:
			client.subscribe(str(topic))

		self.base_canvas.draw_rect((0, 0), (self.top_box_width, self.top_box_height))
		self.base_canvas.draw_text("T:", (0, self.top_text_pos), color=Color.white)
		self.base_canvas.draw_text("ZDL:", (256, self.top_text_pos), color=Color.white)
		self.base_canvas.draw_text("RP:", (512, self.top_text_pos), color=Color.white)
		self.base_canvas.draw_text("PMV:", (768, self.top_text_pos), color=Color.white)
		self.base_canvas.draw_text("MS:", (1024, self.top_text_pos), color=Color.white)

	def on_message(self, client, userdata, msg):
		print(msg.topic + " " + str(msg.payload.decode("utf-8")))
		current_time = round(time.time(), 2)
		if msg.topic == str(topics.PowerModel.recommended_sp):
			parsed_data = self.parse_data(msg.payload)
			self.data["rec_power"] = int(parsed_data["rec_power"])
			self.data["zdist"] = int(parsed_data["zdist"])
		elif msg.topic == str(topics.PowerModel.predicted_max_speed):
			max_speed = str(msg.payload.decode("utf-8"))
			self.data["max_speed"] = float(max_speed)
		elif msg.topic == str(topics.PowerModel.plan_name):
			parsed_data = self.parse_data(msg.payload)
			self.data["plan_name"] = str(parsed_data["plan_name"])
		elif msg.topic == str(topics.DAS.data):
			parsed_data = self.parse_data(msg.payload)
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
				self.data_canvas.clear()

				# Display elapsed time:
				_, rem = divmod(time.time() - self.start_time, 3600)
				minutes, seconds = divmod(rem, 60)
				time_string = "{:0>2}:{:0>2}".format(int(minutes), int(seconds))
				self.data_canvas.draw_text(time_string, (50, self.top_text_pos), color=Color.white)

				# Display power
				if self.data["power"] != 0:
					power = self.data["power"] / self.data["count"]
					rec_power = self.data["rec_power"]
					# Display recommended power
					self.data_canvas.draw_text("{0}".format(round(rec_power, 0)), (600, self.top_text_pos), color=Color.white)
					# Display power (no colour change)
					self.data_canvas.draw_text("P: {0}".format(round(power, 2)), (self.bottom_text_pos_x, self.bottom_text_pos_y), size=self.bottom_text_size, color=Color.red)

				# Display speed
				if int(parsed_data["gps"]) == 1:
					if self.data["gps_speed"] != 0:
						# Predicted max speed
						pred_max_speed = self.data["max_speed"]
						self.data_canvas.draw_text("{0}".format(round(pred_max_speed, 2)), (890, self.top_text_pos), color=Color.white)

						# Actual speed (no colour change)
						speed = self.data["gps_speed"] / self.data["count"]
						self.data_canvas.draw_text("S: {0}".format(round(speed, 2)), (self.bottom_text_pos_x, self.bottom_text_pos_y - self.bottom_text_height), size=self.bottom_text_size, color=Color.red)

						# Actual max speed
						self.data_canvas.draw_text("{0}".format(int(self.actual_max(speed))), (1120, self.top_text_pos), color=Color.white)

				# Display zone distance left (bugged)
				if self.data["zdist"] != 0:
					zdist_left = self.data["zdist"]
					self.data_canvas.draw_text("{0}".format(int(zdist_left)), (360, self.top_text_pos), color=Color.white)

				# Display plan name and clear after 15 secs
				if self.data["plan_name"] != '' and time.time() - self.start_time <= 15:
					plan_name = self.data["plan_name"]
					self.data_canvas.draw_text(plan_name, (0, self.height - 8), color=Color.red)

				# Reset variables
				self.data["power"] = 0
				self.data["cadence"] = 0
				self.data["gps_speed"] = 0
				self.data["reed_distance"] = 0
				self.data["count"] = 0


if __name__ == '__main__':
	my_overlay = OverlayAllStats()
	my_overlay.connect(ip="localhost")
