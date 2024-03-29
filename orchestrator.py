"""Orchestrator Script That Controls The Camera System"""
import argparse
import json
import socket
import sys
import time
from json import dumps
from threading import Timer
import paho.mqtt.client as mqtt

from hardware.hal import get_hal, cleanup

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
    """Get IP address of the raspicam and return the value."""
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
        configs = config.read_configs()
        self.device = configs["device"]

        self.currently_logging = False
        # Used to detect missed start messages
        self.data_messages_received = 0

        self.hal = get_hal(configs["bike"])
        self.hal.mqtt_connected_led.turn_off()
        self.hal.logging_led.turn_off()
        self.hal.logging_button.create_interrupt(self.toggle_logging)

    def toggle_logging(self, _) -> None:
        modules = [topics.WirelessModule.id(i) for i in range(1, 5)]
        for module in modules:
            topic = module.stop if self.currently_logging else module.start
            self.mqtt_client.publish(str(topic))

        # Publish to V3 start topic if button on display is pressed
        next_logging_state = not self.currently_logging
        msg = dumps({"start": next_logging_state})
        self.mqtt_client.publish(str(topics.V3.start), msg)
        print(f"Set logging state to {next_logging_state}")

        # `self.currently_logging` will be updated when we receive the message
        # we publish above.
        # If start message is sent successfully, as we're subscribed to the
        # topic `self.logging_state` will be updated in `on_message`
        # If the message fails to send, we don't update internal logging state
        # so the next button press causes it to try again

    def set_logging_state(self, logging: bool) -> None:
        """Set the data logging state of the camera, updating the LED."""
        self.currently_logging = logging
        if logging:
            self.hal.logging_led.turn_on()
        else:
            self.hal.logging_led.turn_off()

    def publish_camera_status(self) -> None:
        """Send a message on the current device's camera status topic."""
        status_topic = str(topics.Camera.status_camera / self.device)
        message = dumps({"connected": True, "ipAddress": get_ip()})
        self.mqtt_client.publish(status_topic, message, retain=True)

    def battery_loop(self) -> None:
        status_topic = topics.Camera.status_camera / self.device / "battery"
        message = dumps({"voltage": self.hal.battery_adc.read()})
        self.mqtt_client.publish(str(status_topic), message, retain=True)

        Timer(config.BATTERY_PUBLISH_INTERVAL, self.battery_loop).start()

    def on_connect(self, client, userdata, flags, rc):
        """The callback for when the client receives a CONNACK response."""
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(str(topics.Camera.set_overlay))
        client.subscribe(str(topics.Camera.get_overlays))
        client.subscribe(str(topics.WirelessModule.all().module))
        client.subscribe(str(topics.Camera.flip_video_feed / self.device))
        self.publish_camera_status()

        self.hal.mqtt_connected_led.turn_on()
        self.battery_loop()

    def on_message(self, client, userdata, msg):
        """The callback for when a PUBLISH message is received."""
        #print(msg.topic + " " + str(msg.payload))
        if topics.Camera.get_overlays.matches(msg.topic):
            configs = config.read_configs()
            client.publish(
                str(topics.Camera.push_overlays), json.dumps(configs)
            )
        elif topics.Camera.set_overlay.matches(msg.topic):
            config.set_overlay(json.loads(str(msg.payload.decode("utf-8"))))
        elif topics.WirelessModule.all().start.matches(msg.topic):
            self.data_messages_received = 0
            self.set_logging_state(True)
        elif topics.WirelessModule.all().data.matches(msg.topic):
            self.data_messages_received += 1
            # We have 3 WMs, so in the worst case we shouldn't receive more
            # than four messages due to delay after logging stops. If we do,
            # we know we missed the start message.
            if not self.currently_logging and self.data_messages_received > 3:
                self.set_logging_state(True)
        elif topics.WirelessModule.all().stop.matches(msg.topic):
            self.set_logging_state(False)
        elif msg.topic == topics.Camera.flip_video_feed / self.device:
            rotation = config.read_configs().get(config.ROTATION_KEY, 0) + 180
            config.set_rotation(rotation % 360)

    def on_log(self, client, userdata, level, buf):
        """The callback to log all MQTT information"""
        #print("\nlog: ", buf)
        pass

    def on_disconnect(self, client, userdata, msg):
        """The callback called when user is disconnected from the broker."""
        print("Disconnected from broker")
        self.hal.mqtt_connected_led.turn_off()

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
    try:
        orchestrator.start()
    finally:
        cleanup()
