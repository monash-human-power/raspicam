import paho.mqtt.client as mqtt
from time import sleep

"""
A callback function is a function which is:
	- accessible by another function, and
	- is invoked after the first function if that first function completes
"""

# Callback for when client receives a CONNACK response from broker
def on_connect(client, userdata, flags, rc):
	print("Connected with the result code"+str(rc))
	#client.subscribe("cam_sys/DAS/sensors/speed")

# Callback for when message has been sent to broker
# Not working atm, unknow reason
def on_publish(client):
	print("Sent!")

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("172.20.10.10")
client.loop_start()
sleep(0.1)

while True:
	msg = input("Enter message: ")
	topic = "cam_sys/DAS/sensors/speed"
	if msg.lower() == 'quit':
		break
	else:
		client.publish(topic, msg)


