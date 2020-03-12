import time
from enum import Enum
from abc import ABC, abstractmethod
import cv2
import numpy as np
import paho.mqtt.client as mqtt

try:
	from picamera import PiCamera
	ON_PI = True
except (ImportError, RuntimeError):
	ON_PI = False

# Layer 2 is the "preview" (video) layer, hence we skip layers 0, 1 and 2
BASE_LAYER = 3
DATA_LAYER = 4
MESSAGE_LAYER = 5

class Colour(Enum):
	# Remember, OpenCV uses BGR(A) not RGB(A)
	white = (255, 255, 255, 255)
	black = (0, 0, 0, 255)
	transparentBlack = (0, 0, 0, 0)
	blue = (255, 0, 0, 255)
	green = (0, 255, 0, 255)
	red = (0, 0, 255, 255)

class Canvas():
	""" A writeable image, for creating overlay content """

	def __init__(self, width, height):
		""" Initialises to plain black and transparent """
		self.width = width
		self.height = height
		self.img = None
		self.clear()

		if ON_PI:
			self.overlay = None

	def clear(self):
		""" Sets the entire canvas contents to transparentBlack """
		self.img = np.zeros((self.height, self.width, 4), np.uint8)

	@staticmethod
	def _get_colour_tuple(colour):
		""" Internal method - takes a 3-tulpe, 4-tuple or Colour class and returns a 4-tuple colour """
		if isinstance(colour, Colour):
			return colour.value
		if len(colour) == 3:
			return colour + (255,)
		return colour

	def draw_text(self, text, coord, size=1.5, colour=Colour.black):
		""" Draws text to the canvas.
		    The bottom left corner of the text is given by the tuple coord.
		    (the top left of the screen is the origin) """
		colour = Canvas._get_colour_tuple(colour)
		font = cv2.FONT_HERSHEY_SIMPLEX
		# By default thickness = size if thickness isn't specified,
		# but it's a little thin especially on a small screen
		thickness_increase = 0.5
		thickness = round(size + thickness_increase)
		cv2.putText(self.img, text, coord, font, size, colour, thickness, cv2.LINE_AA)

	def draw_rect(self, top_left, bottom_right, colour=Colour.black):
		""" Draws a rectangle to the canvas.
		    top_left and bottom_right are tuples, and specify the dimensions of the rectangle
		    (the top left of the screen is the origin) """
		colour = Canvas._get_colour_tuple(colour)
		cv2.rectangle(self.img, top_left, bottom_right, colour, thickness=cv2.FILLED)

	def copy_to(self, dest):
		""" Writes the contents of self.img over dest, accounting for transparency
		    Use this method to put the overlay contents over the video feed """
		# Extract the alpha mask of the BGRA canvas, convert to BGR
		blue, green, red, alpha = cv2.split(self.img)
		minimum_alpha = 180 # alpha must be > this value to show a pixel
		img = cv2.merge((blue, green, red))
		_, mask = cv2.threshold(alpha, minimum_alpha, 255, cv2.THRESH_BINARY)

		# Black-out the area behind the canvas on the destination
		dest = cv2.bitwise_and(dest, dest, mask=cv2.bitwise_not(mask))
		return cv2.add(dest, img)

	def update_pi_overlay(self, pi_camera: PiCamera, layer: int):
		overlay = pi_camera.add_overlay(self.img, format="rgba", size=(self.width, self.height))
		overlay.layer = layer
		overlay.fullscreen = False
		overlay.window = (0, 20, self.width, self.height)

		# Rather than creating and swapping out overlays, the proper way to do this would be with overlay.update()
		# Unfortunetly, due to a bug in PiCamera 1.13, this will spam us with errors (which don't matter, but still)
		# https://github.com/waveform80/picamera/issues/320
		# https://www.raspberrypi.org/forums/viewtopic.php?t=190120
		if self.overlay:
			pi_camera.remove_overlay(self.overlay)
		self.overlay = overlay

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

		self.base_canvas = Canvas(self.width, self.height)
		self.data_canvas = Canvas(self.width, self.height)
		self.message_canvas = Canvas(self.width, self.height)

		self.client = mqtt.Client()
		self.client.on_connect = self._on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.on_message = self._on_message
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
			"zdist": 0,
			"plan_name": "",
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
			"zdist": float,
			"plan_name": str,
		}

	def get_display(self):
		# Get video feed - source depends on if we're running on a Pi or not
		if ON_PI:
			time.sleep(1)
		else:
			_, frame = self.webcam.read()
			frame = cv2.resize(frame, (self.width, self.height))

			frame = self.base_canvas.copy_to(frame)
			frame = self.data_canvas.copy_to(frame)
			frame = self.message_canvas.copy_to(frame)

			cv2.imshow('frame', self.get_display())
			cv2.waitKey(self.frametime)

	def connect(self, ip="192.168.100.100", port=1883):
		self.client.connect_async(ip, port, 60)

		if ON_PI:
			self.pi_camera.start_preview(fullscreen=False, window=(0, 20, self.width, self.height))

		# mqtt loop (does not block)
		self.client.loop_start()

		# Display video feed and overlay
		while True:
			self.get_display()

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

	def _on_connect(self, client, userdata, flags, rc):
		self.on_connect(client, userdata, flags, rc)
		if ON_PI:
			self.base_canvas.update_pi_overlay(self.pi_camera, BASE_LAYER)

	def _on_message(self, client, userdata, flags):
		self.on_message(client, userdata, flags)
		if ON_PI:
			self.data_canvas.update_pi_overlay(self.pi_camera, DATA_LAYER)

	@abstractmethod
	def on_connect(self, client, userdata, flags, rc):
		pass

	@abstractmethod
	def on_message(self, client, userdata, msg):
		pass