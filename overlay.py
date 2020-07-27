from abc import ABC, abstractmethod
import argparse
import time
from json import dumps
from traceback import format_exc
from typing import Callable

import paho.mqtt.client as mqtt

from backend import BackendFactory
from config import read_configs
from canvas import Canvas
from data import DataFactory, Data
from platform import machine
from topics import DAShboard, Camera

DEFAULT_BIKE = "V2"

class Overlay(ABC):

	def __init__(self, bike, width=1280, height=740, bg: str=None):

		self.width = width
		self.height = height

		# Time between updating the data layer, in seconds
		self.data_update_interval = 1

		self.backend = None
		self.bg_path = None
		# if bg is not None:
		# 	self.backend_name = "opencv_static_image"
		# 	self.bg_path = bg
		# # Raspberry Pis run ARM, PCs run x86_64
		# elif machine() == "armv71":
		# 	self.backend_name = "picamera"
		# else:
		# 	self.backend_name = "opencv"
		self.backend_name = "jesus"

		self.base_canvas = Canvas(self.width, self.height)
		self.data_canvas = Canvas(self.width, self.height)
		self.message_canvas = Canvas(self.width, self.height)

		configs = read_configs()
		bike_version = bike or configs["bike"] or DEFAULT_BIKE
		self.data = DataFactory.create(bike_version)
		self.device = configs["device"]

		self.client = mqtt.Client()
		self.client.on_connect = self._on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.on_log = self.on_log

		self.set_callback_for_topic_list(self.data.get_topics(), self.on_data_message)
		self.set_callback_for_topic_list([str(DAShboard.recording)], self.on_recording_message)

		self.start_time = time.time()

	def publish_errors(self, message: dict, wait_for_publish: bool) -> None:
		""" Sends camera error messages to the MQTT errors topic. Setting the 
			wait_for_publish argument to True will block the broker until the 
			message is published. """
		# Setting up the message
		message['camera'] = self.device
		message['backend'] = self.backend_name
		message['bg_path'] = self.bg_path
		# message['configs'] = configs

		# Publishing the message to the topic
		status_topic = f"{str(Camera.errors)}"
		publish_result = self.client.publish(status_topic, dumps(message))

		if wait_for_publish:
			publish_result.wait_for_publish()

	def publish_recording_status(self, message: str) -> None:
		""" Sends a message on the current device's recording status topic. """
		status_topic = f"{str(DAShboard.recording_status_root)}/{self.device}"
		self.client.publish(status_topic, message, retain=True)

	def connect(self, ip="192.168.100.100", port=1883):
		self.client.connect_async(ip, port, 60)

		with BackendFactory.create(self.backend_name, self.width, self.height, self.publish_recording_status, self.publish_errors) as self.backend:

			if self.backend_name == "opencv_static_image":
				self.backend.set_background(self.bg_path)

			# mqtt loop (does not block)
			self.client.loop_start()

			prev_data_update = 0 # time that we last updated the data layer
			while True:

				# Update the data overlay only if we have waited enough time
				if time.time() > prev_data_update + self.data_update_interval:
					prev_data_update = time.time()

					# Update the data overlay with latest information
					self.update_data_layer()
					self.backend.on_canvases_updated(self.data_canvas, self.message_canvas)

				self.backend.on_loop()

	def set_callback_for_topic_list(self, topics, callback):
		""" Sets the on_message callback for every topic in topics to the
			provided callback """
		for topic in topics:
			self.client.message_callback_add(topic, callback)

	def subscribe_to_topic_list(self, topics):
		""" Constructs a list in the format [("topic1", qos1), ("topic2", qos2), ...]
			see https://pypi.org/project/paho-mqtt/#subscribe-unsubscribe """
		topic_values = list(map(str, topics))
		at_most_once_qos = [0]*len(topics)

		topics_qos = list(zip(topic_values, at_most_once_qos))
		self.client.subscribe(topics_qos)

	def get_data_func(self, data_key: str, decimals=0, scalar=1) -> Callable[[Data], str]:
		""" Returns a lambda function which, when called, returns the current
			value for the data field `data_key`, multiplied by `scalar`, and
			formatted to `decimals` decimal places. """
		format_str = f"{{:.{decimals}f}}"
		return lambda data: format_str.format(data[data_key] * scalar)

	def time_func(self, _: Data) -> str:
		""" Returns the time since the overlay was initialised formatted mm:ss """
		_, rem = divmod(time.time() - self.start_time, 3600)
		minutes, seconds = divmod(rem, 60)
		return "{:0>2}:{:0>2}".format(int(minutes), int(seconds))

	# mqtt methods
	def on_log(self, client, userdata, level, buf):
		print("\nlog: ", buf)

	def on_disconnect(self, client, userdata, msg):
		print("Disconnected from broker")

	def _on_connect(self, client, userdata, flags, rc):
		self.subscribe_to_topic_list(self.data.get_topics())
		self.client.subscribe(str(DAShboard.recording))
		self.on_connect(client, userdata, flags, rc)
		self.backend.on_base_canvas_updated(self.base_canvas)

	def on_data_message(self, client, userdata, msg):
		try:
			payload = msg.payload.decode("utf-8")
			self.data.load_data(msg.topic, payload)
		except:
			self.publish_errors()

	def on_recording_message(self, client, userdata, msg):
		if DAShboard.recording_start.matches(msg.topic):
			self.backend.start_recording()
		elif DAShboard.recording_stop.matches(msg.topic):
			self.backend.stop_recording()

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
		parser.add_argument("--host", action="store", type=str, default="localhost",
			help="Address of the MQTT broker")
		parser.add_argument("-b", "--bike", action="store", type=str,
			choices=["v2", "V2", "v3", "V3"], help="Specify the which bike to expect MQTT data from")
		parser.add_argument("--bg", action="store", type=str,
			help="Replaces the video feed with a static background image at a given location")
		return parser.parse_args()
