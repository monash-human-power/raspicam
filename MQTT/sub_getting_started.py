import paho.mqtt.client as mqtt

# Callback for when client receives a CONNACK response from server(broker?)
def on_connect(client, userdata, flags, rc):
	print("Connected with result code"+str(rc))

	# Subcribing in on_connect() means that if we lose connection and
	# reconnect then subscriptions will be renewed
	client.subscribe("cam_sys/DAS/sensors/speed")

# Callback for when a PUBLISH message is received from server (broker?)
def on_message(client, userdata, msg):
	txt = str(msg.payload)
	print(txt[2:len(txt)-1]) # Slice to remove some characters

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


# connect(host, port=1883, keepalive=60, bind_address="")
client.connect("172.20.10.10", 1883, 60)
client.loop_forever()

