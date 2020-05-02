import argparse
import time
from enum import Enum
from abc import ABC, abstractmethod
import cv2
import numpy as np
import paho.mqtt.client as mqtt

from config import read_configs
from data import Data

try:
	from picamera import PiCamera
	ON_PI = True
except (ImportError, RuntimeError):
	ON_PI = False

# Top of window is outside the screen to hide title bar
PI_WINDOW_TOP_LEFT = (0, -20)
DEFAULT_BIKE = "V2"

class OverlayLayer(Enum):
	video_feed = 2
	base = 3
	data = 4
	message = 5

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
		""" Writes the contents of self.img over dest, accounting for transparency.

		    Use this method to put the overlay contents over the video feed """
		# Extract the alpha mask of the BGRA canvas, convert to BGR
		blue, green, red, alpha = cv2.split(self.img)
		minimum_alpha = 180 # alpha must be > this value to show a pixel
		img = cv2.merge((blue, green, red))
		_, mask = cv2.threshold(alpha, minimum_alpha, 255, cv2.THRESH_BINARY)

		# Black-out the area behind the canvas on the destination
		dest = cv2.bitwise_and(dest, dest, mask=cv2.bitwise_not(mask))
		return cv2.add(dest, img)

	def update_pi_overlay(self, pi_camera, layer):
		""" Adds the overlay to a PiCamera preview, and if the overlay was already added,
		    removes the old instance. """
		overlay = pi_camera.add_overlay(self.img, format="rgba", size=(self.width, self.height))
		overlay.layer = layer
		overlay.fullscreen = False
		overlay.window = (*PI_WINDOW_TOP_LEFT, self.width, self.height)

		# Rather than creating and swapping out overlays, the proper way to do this would be with overlay.update()
		# Unfortunately, due to a bug in PiCamera 1.13, this will spam us with errors (which don't matter, but still)
		# https://github.com/waveform80/picamera/issues/320
		# https://www.raspberrypi.org/forums/viewtopic.php?t=190120
		if self.overlay:
			pi_camera.remove_overlay(self.overlay)
		self.overlay = overlay

class Overlay(ABC):

	def __init__(self, width=1280, height=740):

		self.width = width
		self.height = height

		# Time between video frames when running on OpenCV, in milliseconds
		self.frametime = 17
		# Time between updating the data layer, in seconds
		self.data_update_interval = 1

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

		configs = read_configs()
		self.data = Data.get_data_instance(configs["bike"] or DEFAULT_BIKE)

		self.client = mqtt.Client()
		self.client.on_connect = self._on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.on_message = self._on_message
		self.client.on_log = self.on_log

	def show_opencv_frame(self):
		""" Creates the frame using the webcam and canvases, and displays result """
		_, frame = self.webcam.read()
		frame = cv2.resize(frame, (self.width, self.height))

		frame = self.base_canvas.copy_to(frame)
		frame = self.data_canvas.copy_to(frame)
		frame = self.message_canvas.copy_to(frame)

		cv2.imshow('frame', frame)
		cv2.waitKey(self.frametime)

	def connect(self, ip="192.168.100.100", port=1883):
		self.client.connect_async(ip, port, 60)

		if ON_PI:
			# Start displaying video feed. Non blocking, but runs forever.
			self.pi_camera.start_preview(fullscreen=False, window=(*PI_WINDOW_TOP_LEFT, self.width, self.height))

		# mqtt loop (does not block)
		self.client.loop_start()

		prev_data_update = 0 # time that we last updated the data layer
		while True:

			# Update the data overlay only if we have waited enough time
			if time.time() > prev_data_update + self.data_update_interval:
				prev_data_update = time.time()

				# Update the data overlay with latest information
				self.update_data_layer()

				if ON_PI:
					# Update the overlay images on picamera. Picamera will
					# retain the overlay images until updated, so we only need
					# to do this once per overlay update.
					self.data_canvas.update_pi_overlay(self.pi_camera, OverlayLayer.data)
					self.message_canvas.update_pi_overlay(self.pi_camera, OverlayLayer.message)

			if not ON_PI:
				# Create and display the frame using OpenCV.
				# This function fetches the most up-to-date overlay, as OpenCV
				# needs us to manually add it to each frame.
				self.show_opencv_frame()

	def subscribe_to_topic_list(self, topics):
		# https://pypi.org/project/paho-mqtt/#subscribe-unsubscribe
		# Basically, construct a list in the format [("topic1", qos1), ("topic2", qos2), ...]
		topic_values = list(map(str, topics))
		at_most_once_qos = [0]*len(topics)

		topics_qos = list(zip(topic_values, at_most_once_qos))
		self.client.subscribe(topics_qos)

	# Calculate max speed
	def actual_max(self, cur_speed):
		return max(self.max_speed, cur_speed)

	# mqtt methods
	def on_log(self, client, userdata, level, buf):
		print("\nlog: ", buf)

	def on_disconnect(self, client, userdata, msg):
		print("Disconnected from broker")

	def _on_connect(self, client, userdata, flags, rc):
		self.subscribe_to_topic_list(self.data.get_topics())
		self.on_connect(client, userdata, flags, rc)
		if ON_PI:
			self.base_canvas.update_pi_overlay(self.pi_camera, OverlayLayer.base)

	def _on_message(self, client, userdata, msg):
		payload = msg.payload.decode("utf-8")
		self.data.load_data(msg.topic, payload)

	@abstractmethod
	def on_connect(self, client, userdata, flags, rc):
		""" Called automatically when the overlay connects successfully to the
			MQTT broker.

			Overlay implementations may override for one-off operations
			(e.g. drawing self.base_canvas) """
		pass

	@abstractmethod
	def update_data_layer(self):
		""" Called automatically at a regular interval defined by
			self.data_update_interval.

			Overlay implementations should override this method with code which
			updates self.data_canvas. """
		pass

	@staticmethod
	def get_overlay_args(overlay_description: str):
		parser = argparse.ArgumentParser(description=overlay_description, add_help=True)
		parser.add_argument("--host", action="store", type=str, default="localhost", help="Address of the MQTT broker")
		return parser.parse_args()
