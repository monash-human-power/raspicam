import time
from overlay import Overlay, Colour

class OverlayAllStats(Overlay):

	def __init__(self):
		super(OverlayAllStats, self).__init__()
		self.text_height = 50
		self.speed_height = 70
		self.message_received_time = 0

	def on_connect(self, client, userdata, flags, rc):
		print('Connected with rc: {}'.format(rc))

		# Add static text
		self.base_canvas.draw_text("REC Power:", (5, self.text_height * 1))
		self.base_canvas.draw_text("Power:", (5, self.text_height * 2))
		self.base_canvas.draw_text("Cadence:", (5, self.text_height * 3))
		self.base_canvas.draw_text("Distance:", (5, self.text_height * 4))
		self.base_canvas.draw_text("Message:", (5, self.text_height * 5 ), size = 1)

		speed_x = self.width // 2 - 300
		self.base_canvas.draw_text("SP:", (speed_x, self.height - self.speed_height * 0), size=2.5)
		self.base_canvas.draw_text("REC:", (speed_x, self.height - self.speed_height * 1), size=2.5)
		self.base_canvas.draw_text("MAX:", (speed_x, self.height - self.speed_height * 2), size=2.5)

	def update_data_layer(self):
		self.data_canvas.clear()
		self.message_canvas.clear()

		# Display power
		if self.data["power"] != 0:
			power = self.data["power"]
			rec_power = self.data["rec_power"]
			tolerance = 0.05
			# Display recommended power
			self.data_canvas.draw_text("{0}".format(round(rec_power, 2)), (340, self.text_height * 1))
			# Display power
			if power > (rec_power + (rec_power * tolerance)):
				power_colour = Colour.red
			elif power > rec_power:
				power_colour = Colour.green
			else:
				power_colour = Colour.black
			self.data_canvas.draw_text("{0}".format(round(power, 2)), (340, self.text_height * 2), colour=power_colour)

		# Display cadence
		if self.data["cadence"] != 0:
			cadence = self.data["cadence"]
			self.data_canvas.draw_text("{0}".format(round(cadence, 2)), (340, self.text_height * 3))

		# Display speed
		if self.data["reed_velocity"] != 0:
			# Max Speed
			max_speed = self.data["predicted_max_speed"]
			max_speed_text = "{0} km/h".format(round(max_speed, 2))
			max_speed_pos = (self.width // 2 - 70, self.height - self.speed_height * 2)
			self.data_canvas.draw_text(max_speed_text, max_speed_pos, size=2.5)

			# Recommended speed
			rec_speed = self.data["rec_speed"]
			rec_speed_text = "{0} km/h".format(round(rec_speed, 2))
			rec_speed_pos = (self.width // 2 - 70, self.height - self.speed_height * 1)
			self.data_canvas.draw_text(rec_speed_text, rec_speed_pos, size=2.5)

			# Actual speed
			speed = self.data["reed_velocity"]
			speed_text = "{0} km/h".format(round(speed, 2))
			speed_pos = (self.width // 2 - 70, self.height - self.speed_height * 0)
			tolerance = 0.05
			if speed > (rec_speed + (rec_speed * tolerance)):
				speed_colour = Colour.red
			elif speed > rec_speed:
				speed_colour = Colour.green
			else:
				speed_colour = Colour.black
			self.data_canvas.draw_text(speed_text, speed_pos, colour=speed_colour, size=2.5)

		# Display reed_distance (distance travelled)
		if self.data["reed_distance"] != 0:
			reed_distance = self.data["reed_distance"]
			self.data_canvas.draw_text("{0}".format(round(reed_distance, 2)), (340, self.text_height * 4))
		
		# Display messages from DAShboard
		if self.data.has_message():
			message = self.data.get_message()
			self.message_canvas.draw_text(message, (190, self.text_height * 5), size=1, colour=Colour.red)

if __name__ == '__main__':
	args = Overlay.get_overlay_args("Overlay displaying all (or just many) statistics")
	my_overlay = OverlayAllStats()
	my_overlay.connect(ip=args.host)