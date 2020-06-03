from abc import ABC, abstractmethod
import argparse
from json import dumps
from os import mkdir, path
from shutil import disk_usage
import time
from traceback import format_exc

import paho.mqtt.client as mqtt

from config import read_configs
from canvas import Canvas
from data import DataFactory
from backend import get_backend
from topics import DAShboard

DEFAULT_BIKE = "V2"

class Overlay(ABC):

	def __init__(self, bike, width=1280, height=740):

		self.width = width
		self.height = height

		# Time between updating the data layer, in seconds
		self.data_update_interval = 1
		# Time between recording statuses, in seconds
		self.recording_status_interval = 60
		# time that we last called self.send_recording_status
		self.prev_recording_status = 0

		self.max_speed = float('-inf')
		self.start_time = round(time.time(), 2)

		self.backend = get_backend()

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

	def connect(self, ip="192.168.100.100", port=1883):
		self.client.connect_async(ip, port, 60)

		with self.backend(self.width, self.height):

			# mqtt loop (does not block)
			self.client.loop_start()

			prev_data_update = 0 # time that we last updated the data layer
			while True:

				# Update the data overlay only if we have waited enough time
				if time.time() > prev_data_update + self.data_update_interval:
					prev_data_update = time.time()

					# Update the data overlay with latest information
					self.update_data_layer()
					self.backend.on_overlays_updated()

				if time.time() > self.prev_recording_status + self.recording_status_interval:
					self.send_recording_status()

				self.backend.on_loop()

	def start_recording(self):
		""" Starts an h264 recording with the first available name located in
			the recordings folder.

			Should be paired with a call to stop_recording. Must be running
			with picamera. """
		output_folder = path.dirname(path.realpath(__file__)) + "/recordings"
		output_file_pattern = f"{output_folder}/rec_{{}}.h264"

		if not path.exists(output_folder):
			mkdir(output_folder)

		video_number = 1
		while path.exists(output_file_pattern.format(video_number)):
			video_number += 1
		self.recording_output_file = output_file_pattern.format(video_number)

		try:
			self.pi_camera.start_recording(self.recording_output_file)
			self.recording_start_time = time.time()
			self.pi_camera.wait_recording(0.1)
			self.send_recording_status()
		except Exception:
			self.send_recording_error()

	def stop_recording(self):
		""" Stops and saves any current recording at the location found in
			start_recording().

			No action is taken if there was no recording in progress. Must be
			running with picamera. """

		try:
			if self.pi_camera.recording:
				self.pi_camera.stop_recording()
			self.send_recording_status()
		except Exception:
			self.send_recording_error()

	def send_recording_status(self):
		""" Checks if any errors have occured with recording, and sends the
			current recording status via MQTT """
		message = {}

		if ON_PI and self.pi_camera.recording:
			try:
				self.pi_camera.wait_recording()
				message["status"] = "recording"
				message["recordingMinutes"] = (time.time() - self.recording_start_time) / 60
				message["recordingFile"] = self.recording_output_file

			except Exception:
				self.send_recording_error()
				return
		else:
			message["status"] = "off"
		_, _, free_disk_space = disk_usage(__file__)
		message["diskSpaceRemaining"] = free_disk_space

		status_topic = f"{str(DAShboard.recording_status_root)}/{self.device}"
		self.client.publish(status_topic, dumps(message), retain=True)

		self.prev_recording_status = time.time()

	def send_recording_error(self):
		""" Sends the most recent exception to the recording status MQTT topic """
		_, _, free_disk_space = disk_usage(__file__)
		message = {
			"status": "error",
			"error": format_exc(),
			"diskSpaceRemaining": free_disk_space,
		}
		status_topic = f"{str(DAShboard.recording_status_root)}/{self.device}"
		self.client.publish(status_topic, dumps(message), retain=True)
		print(format_exc())

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
		self.client.subscribe(str(DAShboard.recording))
		self.on_connect(client, userdata, flags, rc)
		self.backend.on_base_overlay_update(self.base_canvas)

	def on_data_message(self, client, userdata, msg):
		payload = msg.payload.decode("utf-8")
		self.data.load_data(msg.topic, payload)

	def on_recording_message(self, client, userdata, msg):
		if not ON_PI:
			print("WARNING: Recording is not yet possible with OpenCV")
			return
		if DAShboard.recording_start.matches(msg.topic):
			self.start_recording()
		elif DAShboard.recording_stop.matches(msg.topic):
			self.stop_recording()

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
		return parser.parse_args()
