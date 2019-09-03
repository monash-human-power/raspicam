import json
import configs
import argparse
import time
import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default="192.168.100.100", help="ip address of the broker")
args = parser.parse_args()

broker_ip = args.host


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("camera/set_overlay")
	client.subscribe("camera/get_overlays")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))
	if msg.topic == "camera/get_overlays":
		configs = configs.read_configs()
		client.publish("camera/push_overlays", json.dumps(configs))
	elif msg.topic == "camera/set_overlay":
		configs.set_overlay(json.loads(str(msg.payload.decode("utf-8"))))


def on_log(client, userdata, level, buf):
	print("\nlog: ", buf)


def on_disconnect(client, userdata, msg):
	print("Disconnected from broker")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log
client.on_disconnect = on_disconnect

client.connect_async(broker_ip, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()
while True:
	time.sleep(1)
