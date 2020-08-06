"""Orchestrator Script That Controls The Camera System"""
import json
import argparse
import sys
import time
import paho.mqtt.client as mqtt
import config
import topics


def get_args(argv=[]):
    """Get arguments passed into Python script"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        type=str,
        default="192.168.100.100",
        help="ip address of the broker",
    )
    return parser.parse_args(argv)


class Orchestrator:
    def __init__(self, broker_ip, port=1883):

        self.broker_ip = broker_ip
        self.port = port
        self.mqtt_client = None

    def on_connect(self, client, userdata, flags, rc):
        """The callback for when the client receives a CONNACK response from the server."""
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(str(topics.Camera.set_overlay))
        client.subscribe(str(topics.Camera.get_overlays))

    def on_message(self, client, userdata, msg):
        """The callback for when a PUBLISH message is received from the server."""
        print(msg.topic + " " + str(msg.payload))
        if topics.Camera.get_overlays.matches(msg.topic):
            configs = config.read_configs()
            client.publish(
                str(topics.Camera.push_overlays), json.dumps(configs)
            )
        elif topics.Camera.set_overlay.matches(msg.topic):
            config.set_overlay(json.loads(str(msg.payload.decode("utf-8"))))

    def on_log(self, client, userdata, level, buf):
        """The callback to log all MQTT information"""
        print("\nlog: ", buf)

    def on_disconnect(self, client, userdata, msg):
        """ The callback that is called when user is disconnected from broker"""
        print("Disconnected from broker")

    def start(self):
        """start Orchestrator"""
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_log = self.on_log
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.connect_async(self.broker_ip, self.port, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
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
