"""Orchestrator Script That Controls The Camera System"""
import argparse
import json
import sys
import time
import socket

import paho.mqtt.client as mqtt

from mhp import topics

import config


def get_args(argv=[]):
    """Get arguments passed into Python script"""
    configs = config.read_configs()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--host",
        type=str,
        default=configs["broker_ip"],
        help="ip address of the broker",
    )
    return parser.parse_args(argv)


def get_ip():
    """ Get IP address of the raspicam and return the value. """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Any IP address should work
        # Source: https://stackoverflow.com/a/28950776
        s.connect(("192.168.100.100", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class Orchestrator:
    def __init__(self, broker_ip, port=1883):

        self.broker_ip = broker_ip
        self.port = port
        self.mqtt_client = None
        self.configs = config.read_configs()
        self.device = self.configs["device"] 

    def publish_camera_status(self) -> None:
        """ Send a message on the current device's camera status topic. """
        message = json.dumps(
            {
                "connected": True, 
                "ip_address": get_ip(),
                "brightness": self.configs["brightness"], 
                "contrast": self.configs["contrast"]
            }
        )
        status_topic = str(topics.Camera.status_camera / self.device)
        self.mqtt_client.publish(status_topic, message, retain=True)

    def on_connect(self, client, userdata, flags, rc):
        """The callback for when the client receives a CONNACK response."""
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(str(topics.Camera.set_overlay))
        client.subscribe(str(topics.Camera.get_overlays))
        client.subscribe(str(topics.Camera.status_camera / self.device))
        self.publish_camera_status()

    def on_message(self, client, userdata, msg):
        """The callback for when a PUBLISH message is received."""
        print(msg.topic + " " + str(msg.payload))
        if topics.Camera.get_overlays.matches(msg.topic):
            configs = config.read_configs()
            client.publish(
                str(topics.Camera.push_overlays), json.dumps(configs)
            )
        elif topics.Camera.set_overlay.matches(msg.topic):
            config.set_overlay(json.loads(str(msg.payload.decode("utf-8"))))
        elif (topics.Camera.status_camera / self.device).matches(msg.topic):
            message = json.loads(msg.payload.decode("utf-8"))
            brightness = message["brightness"]
            contrast = message["contrast"]
            config.write_to_configs("brightness", brightness)
            config.write_to_configs("contrast", contrast)

    def on_log(self, client, userdata, level, buf):
        """The callback to log all MQTT information"""
        print("\nlog: ", buf)

    def on_disconnect(self, client, userdata, msg):
        """The callback called when user is disconnected from the broker."""
        print("Disconnected from broker")

    def start(self):
        """start Orchestrator"""
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_log = self.on_log
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.connect_async(self.broker_ip, self.port, 60)

        # Set the camera status to offline if connection breaks
        camera_topic = str(topics.Camera.status_camera / self.device)
        self.mqtt_client.will_set(
            camera_topic, dumps({"connected": False}), 1, True
        )

        # Blocking call that processes network traffic, dispatches callbacks
        # and handles reconnecting.
        # Other loop*() functions are available that give a threaded interface
        # and a manual interface.
        self.mqtt_client.loop_start()
        while True:
            time.sleep(1)


if __name__ == "__main__":
    # Get command line arguments
    ARGS = get_args(sys.argv[1:])
    BROKER_IP = ARGS.host
    orchestrator = Orchestrator(BROKER_IP)

    # Start
    orchestrator.start()
