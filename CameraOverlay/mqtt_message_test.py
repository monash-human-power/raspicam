""" MQTT Test Script For Sending Messages To CameraOverlay """

import paho.mqtt.client as mqtt
import time

def on_log(client, userdata, level, buf):
    print("log: "+buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_diconnect(client, userdata, flags, rc = 0):
    print("Disconnected result code "+str(rc))

broker = "localhost"
client = mqtt.Client("python1")

client.on_log = on_log
client.on_connect = on_connect
client.on_diconnect = on_diconnect

print("Connecting to broker", broker)
client.connect(broker)

# Sending Messages Every 8 seconds
client.loop_start()
time.sleep(1)
while True:
    client.publish("v3/camera-system/primary/message", "Test Message")
    time.sleep(8)