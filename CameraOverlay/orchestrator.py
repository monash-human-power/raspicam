"""Orchestrator script that controls the camera system"""
import json
import argparse
import time
import paho.mqtt.client as mqtt
import config
import topics


def get_args(argv=None):
    """Get arguments passed into Python script"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str,
                        default="192.168.100.100",
                        help="ip address of the broker")
    return parser.parse_args(argv)


def on_connect(client, userdata, flags, rc):
    """The callback for when the client receives a CONNACK response from the server."""
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topics.Camera.set_overlay)
    client.subscribe(topics.Camera.get_overlays)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == topics.Camera.get_overlays:
        configs = config.read_configs()
        client.publish(topics.Camera.push_overlays, json.dumps(configs))
    elif msg.topic == topics.Camera.set_overlay:
        config.set_overlay(json.loads(str(msg.payload.decode("utf-8"))))


def on_log(client, userdata, level, buf):
    """The callback to log all MQTT information"""
    print("\nlog: ", buf)


def on_disconnect(client, userdata, msg):
    """ The callback that is called when user is disconnected from broker"""
    print("Disconnected from broker")


if __name__ == '__main__':
    # Get command line arguments
    ARGS = get_args()
    BROKER_IP = ARGS.host

    # Start
    MQTT_CLIENT = mqtt.Client()
    MQTT_CLIENT.on_connect = on_connect
    MQTT_CLIENT.on_message = on_message
    MQTT_CLIENT.on_log = on_log
    MQTT_CLIENT.on_disconnect = on_disconnect

    MQTT_CLIENT.connect_async(BROKER_IP, 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    MQTT_CLIENT.loop_start()
    while True:
        time.sleep(1)
