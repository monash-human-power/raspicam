import time
from overlay import Overlay, Colour


class OverlayTopStrip(Overlay):

	def __init__(self):
		super(OverlayTopStrip, self).__init__()

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

		self.base_canvas.draw_rect((0, 0), (self.top_box_width, self.top_box_height))
		self.base_canvas.draw_text("T:", (0, self.top_text_pos), colour=Colour.white)
		self.base_canvas.draw_text("ZDL:", (256, self.top_text_pos), colour=Colour.white)
		self.base_canvas.draw_text("RP:", (512, self.top_text_pos), colour=Colour.white)
		self.base_canvas.draw_text("PMV:", (768, self.top_text_pos), colour=Colour.white)
		self.base_canvas.draw_text("MS:", (1024, self.top_text_pos), colour=Colour.white)

	def update_data_layer(self):
		# Create a transparent image to attach text
		self.data_canvas.clear()

		# Display elapsed time:
		_, rem = divmod(time.time() - self.start_time, 3600)
		minutes, seconds = divmod(rem, 60)
		time_string = "{:0>2}:{:0>2}".format(int(minutes), int(seconds))
		self.data_canvas.draw_text(time_string, (50, self.top_text_pos), colour=Colour.white)

		if self.data["power"] != 0:
			self.draw_power_rec_power()

		if self.data["gps"] == 1:
			if self.data["gps_speed"] != 0:
				self.draw_speed_max_speed()

		# Display zone distance left (bugged)
		if self.data["zdist"] != 0:
			self.draw_zone_dist()

		# Display plan name and clear after 15 secs
		if self.data["plan_name"] != '' and time.time() - self.start_time <= 15:
			self.draw_plan_name()

	def draw_power_rec_power(self):
		power = self.data["power"]
		rec_power = self.data["rec_power"]
		# Display recommended power
		self.data_canvas.draw_text("{0}".format(round(rec_power, 0)), (600, self.top_text_pos), colour=Colour.white)
		# Display power (no colour change)
		self.data_canvas.draw_text("P: {0}".format(round(power, 2)), (self.bottom_text_pos_x, self.bottom_text_pos_y), size=self.bottom_text_size, colour=Colour.red)

	def draw_speed_max_speed(self):
		# Predicted max speed
		pred_max_speed = self.data["predicted_max_speed"]
		self.data_canvas.draw_text("{0}".format(round(pred_max_speed, 1)), (890, self.top_text_pos), colour=Colour.white)

		# Actual speed (no colour change)
		speed = self.data["gps_speed"]
		self.data_canvas.draw_text("S: {0}".format(round(speed, 2)), (self.bottom_text_pos_x, self.bottom_text_pos_y - self.bottom_text_height), size=self.bottom_text_size, colour=Colour.red)

		# Actual max speed
		self.data_canvas.draw_text("{0}".format(int(self.actual_max(speed))), (1120, self.top_text_pos), colour=Colour.white)

	def draw_zone_dist(self):
		zdist_left = self.data["zdist"]
		self.data_canvas.draw_text("{0}".format(int(zdist_left)), (360, self.top_text_pos), colour=Colour.white)

	def draw_plan_name(self):
		plan_name = self.data["plan_name"]
		self.data_canvas.draw_text(plan_name, (0, self.height - 8), colour=Colour.red)

if __name__ == '__main__':
	args = Overlay.get_overlay_args("Shows important statistics in a bar at the top of the screen")
	my_overlay = OverlayTopStrip()
	my_overlay.connect(ip=args.host)
