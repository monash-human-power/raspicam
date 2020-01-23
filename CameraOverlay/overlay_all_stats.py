import time
from overlay import Overlay, Colour
import topics

class OverlayAllStats(Overlay):

	topics = [
			topics.DAS.start,
			topics.DAS.data,
			topics.DAS.stop,
			topics.PowerModel.recommended_sp,
			topics.PowerModel.max_speed,
			topics.DAShboard.recieve_message,
	]

	def __init__(self):
		super(OverlayAllStats, self).__init__()
		self.text_height = 50
		self.speed_height = 70

	def on_connect(self, client, userdata, flags, rc):
		print('Connected with rc: {}'.format(rc))

		# https://pypi.org/project/paho-mqtt/#subscribe-unsubscribe
		# Basically, construct a list in the format [("topic1", qos1), ("topic2", qos2), ...]
		topic_values = list(map(str, OverlayAllStats.topics))
		at_most_once_qos = [0]*len(OverlayAllStats.topics)

		topics_qos = list(zip(topic_values, at_most_once_qos))
		client.subscribe(topics_qos)

		# Add static text
		self.base_canvas.draw_text("REC Power:", (5, self.text_height * 1))
		self.base_canvas.draw_text("Power:", (5, self.text_height * 2))
		self.base_canvas.draw_text("Cadence:", (5, self.text_height * 3))
		self.base_canvas.draw_text("Distance:", (5, self.text_height * 4))
		self.base_canvas.draw_text("Message:", (5,self.text_height * 5 ),size = 1)

		speed_x = self.width // 2 - 300
		self.base_canvas.draw_text("SP:", (speed_x, self.height - self.speed_height * 0), size=2.5)
		self.base_canvas.draw_text("REC:", (speed_x, self.height - self.speed_height * 1), size=2.5)
		self.base_canvas.draw_text("MAX:", (speed_x, self.height - self.speed_height * 2), size=2.5)

	def on_message(self, client, userdata, msg):
		topic = msg.topic
		print(topic + " " + str(msg.payload.decode("utf-8")))
		current_time = round(time.time(), 2)

		if topic == str(topics.PowerModel.recommended_sp):
			parsed_data = self.parse_data(msg.payload)
			self.data["rec_power"] = float(parsed_data["rec_power"])
			self.data["rec_speed"] = float(parsed_data["rec_speed"])
		elif topic == str(topics.PowerModel.max_speed):
			max_speed = str(msg.payload.decode("utf-8"))
			self.data["max_speed"] = float(max_speed)
		elif topic == str(topics.DAS.data):
			data = msg.payload
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
				self.data_canvas.clear()

				# Display power
				if self.data["power"] != 0:
					power = self.data["power"] / self.data["count"]
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
					cadence = self.data["cadence"] / self.data["count"]
					self.data_canvas.draw_text("{0}".format(round(cadence, 2)), (340, self.text_height * 3))

				# Display speed
				if self.data["reed_velocity"] != 0:
					# Max Speed
					max_speed = self.data["max_speed"]
					max_speed_text = "{0} km/h".format(round(max_speed, 2))
					max_speed_pos = (self.width // 2 - 70, self.height - self.speed_height * 2)
					self.data_canvas.draw_text(max_speed_text, max_speed_pos, size=2.5)

					# Recommended speed
					rec_speed = self.data["rec_speed"]
					rec_speed_text = "{0} km/h".format(round(rec_speed, 2))
					rec_speed_pos = (self.width // 2 - 70, self.height - self.speed_height * 1)
					self.data_canvas.draw_text(rec_speed_text, rec_speed_pos, size=2.5)

					# Actual speed
					speed = self.data["reed_velocity"] / self.data["count"]
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
					reed_distance = self.data["reed_distance"] / self.data["count"]
					self.data_canvas.draw_text("{0}".format(round(reed_distance, 2)), (340, self.text_height * 4))

				# Reset variables
				self.data["power"] = 0
				self.data["cadence"] = 0
				self.data["gps_speed"] = 0
				self.data["reed_velocity"] = 0
				self.data["reed_distance"] = 0
				self.data["count"] = 0
		
		elif topic == str(topics.DAShboard.recieve_message):
			message = msg.payload.decode("utf-8")

			# reset counter once message is recieved 
			self.frame_counter = 0  

			# Display Message
			self.message_canvas.draw_text("{0}".format(message), (190, self.text_height * 5), size= 1, colour=Colour.red)
		
		if self.frame_counter >= 70:
			self.message_canvas.clear()

if __name__ == '__main__':
	my_overlay = OverlayAllStats()
	my_overlay.connect(ip="localhost")
