import time
from abc import ABC, abstractmethod
import cv2
import numpy as np
import paho.mqtt.client as mqtt

try:
	from picamera import PiCamera, PiRGBArray
	ON_PI = True
except (ImportError, RuntimeError):
	ON_PI = False

def add_overlay_to_frame(frame, overlay):
	# Extract the alpha mask of the BGRA overlay, convert to BGR
	blue, green, red, alpha = cv2.split(overlay)
	overlay = cv2.merge((blue, green, red))
	_, mask = cv2.threshold(alpha, 180, 255, cv2.THRESH_BINARY)

	# Black-out the area behind the overlay
	frame = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
	return cv2.add(frame, overlay)

class Overlay(ABC):

	def __init__(self, width=1280, height=740):
		self.width = width
		self.height = height
		self.frametime = 17 # ms

		self.prev_overlay = None
		self.max_speed = float('-inf')
		self.start_time = round(time.time(), 2)

		if ON_PI:
			self.pi_camera = PiCamera(resolution=(self.width, self.height))
		else:
			self.webcam = cv2.VideoCapture(0)

		self.base_overlay = np.zeros((self.height, self.width, 4), np.uint8)
		self.data_overlay = np.zeros((self.height, self.width, 4), np.uint8)

		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.on_message = self.on_message
		self.client.on_log = self.on_log

		self.data = {
			# das data
			"count": 0,
			"cadence": 0,
			"gps": 0,
			"gps_speed": 0,
			"power": 0,
			"reed_distance": 0,
			"reed_velocity": 0,

			# power model data
			"max_speed": 0,
			"rec_power": 0,
			"rec_speed": 0,
		}

		self.data_types = {
			# das data
			"power": int,
			"cadence": int,
			"reed_velocity": float,
			"gps": int,
			"gps_speed": float,
			"reed_distance": float,
			"count": int,

			# power model data
			"rec_power": float,
			"rec_speed": float,
			"max_speed": float,
		}

	# self.topics = [
	#
	# ]

	def get_display(self):
		# Get video feed - source depends on if we're running on a Pi or not
		if ON_PI:
			raw_capture = PiRGBArray(self.pi_camera)
			self.pi_camera.capture(raw_capture, format="bgr")
			frame = raw_capture.array
		else:
			_, frame = self.webcam.read()
			frame = cv2.resize(frame, (self.width, self.height))

		# First do the base overlay:
		frame = add_overlay_to_frame(frame, self.base_overlay)
		frame = add_overlay_to_frame(frame, self.data_overlay)

		return frame

	def connect(self, ip="192.168.100.100", port=1883):
		self.client.connect_async(ip, port, 60)

		# mqtt loop (does not block)
		self.client.loop_start()

		# Display video feed and overlay
		while True:
			cv2.imshow('frame', self.get_display())
			cv2.waitKey(self.frametime)

	# Convert data to a suitable format
	def parse_data(self, data):
		terms = data.decode("utf-8").split("&")
		data_dict = {}
		for term in terms:
			key, value = term.split("=")
			if key not in self.data_types:
				continue
			cast_func = self.data_types[key]
			data_dict[key] = cast_func(value)
		return data_dict

	# Calculate max speed
	def actual_max(self, cur_speed):
		return max(self.max_speed, cur_speed)

	# mqtt methods
	def on_log(self, client, userdata, level, buf):
		print("\nlog: ", buf)

	def on_disconnect(self, client, userdata, msg):
		print("Disconnected from broker")

	def subscribe_topics(self, topics):
		self.client.subscribe(topics)

	def reset_variables(self, value=0):
		for key, _ in self.data.items():
			self.data[key] = value

	@abstractmethod
	def on_connect(self, client, userdata, flags, rc):
		pass

	@abstractmethod
	def on_message(self, client, userdata, msg):
		pass
