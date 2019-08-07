from picamera import PiCamera
import time
import paho.mqtt.client as mqtt
from abc import ABC, abstractmethod


class Overlay(ABC):
	def __init__(self, width=1280, height=740):
		self.width = width
		self.height = height

		self.prev_overlay = None
		self.max_speed = float('-inf')
		self.start_time = round(time.time(), 2)

		self.camera = PiCamera(resolution=(self.width, self.height))

		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.on_message = self.on_message
		self.client.on_log = self.on_log

	@property
	def data(self):
		return NotImplementedError

	@property
	def data_types(self):
		return NotImplementedError

	def get_value(self, value):
		cast_func = self.data_types[value]
		parsed_value = self.parse_data(self.data[value])
		casted_value = cast_func(parsed_value)
		return casted_value

	def connect(self, ip, port):
		self.client.connect_async(ip, port, 60)

		# mqtt loop
		# Position and size of the preview window(x,y,width,height)
		self.camera.start_preview(fullscreen=False, window=(0, -20, self.width, self.height))
		self.client.loop_start()
		while True:
			time.sleep(1)

	# Convert data to a suitable format
	def parse_data(self, data):
		terms = data.decode("utf-8").split("&")
		data_dict = {}
		for term in terms:
			key, value = term.split("=")
			data_dict[key] = value
		return data_dict

	# Calculate max speed
	def actual_max(self, cur_speed):
		return max(self.max_speed, cur_speed)

	# mqtt methods
	def on_log(client, userdata, level, buf):
		print("\nlog: ", buf)

	def on_disconnect(client, userdata, msg):
		print("Disconnected from broker")

	def subscribe_topics(self, topics):
		self.client.subscribe(topics)

	@abstractmethod
	def update_overlay(self, data):
		pass

	@abstractmethod
	def on_connect(self, client, userdata, flags, rc):
		pass

	@abstractmethod
	def on_message(self, client, userdata, msg):
		pass
