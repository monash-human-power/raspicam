
from picamera import PiCamera, Color
from PIL import Image, ImageDraw, ImageFont
import time
import datetime as dt
import paho.mqtt.client as mqtt
import json

speed_height = 70
speed_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',speed_height)
text_height = 45
text_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',text_height)

brokerIP = "192.168.100.100"

PREV_OVERLAY = None
START_TIME = round(time.time(), 2)
GLOBAL_DATA = {
    "power": 0,
    "cadence": 0,
    "gps_speed": 0,
    "reed_distance": 0,
    "count": 0,
}

REQUIRED_DATA = {
    "rec_power": 0,
    "rec_speed": 0,
    "max_speed": 0,
}

# The resolution of the camera preview. Current system using 800x480.
WIDTH = 1280
HEIGHT = 800

# Initiate camera preview
camera = PiCamera(resolution=(WIDTH, HEIGHT))

# Convert data to a suitable format
def parse_data(data):
    terms = data.split("&")
    data_dict = {}
    filename = ""
    for term in terms:
        key,value = term.split("=")
        data_dict[key] = value
    return data_dict

# mqtt methods
def on_log(client, userdata, level, buf):
    print("\nlog: ", buf)
    
def on_disconnect(client, userdata, msg):
    print("Disconnected from broker")

def on_connect(client, userdata, flags, rc):
    print("Connected with rc: " + str(rc))
    client.subscribe("start")
    client.subscribe("data")
    client.subscribe("stop")
    client.subscribe("power_model/recommended_SP")
    client.subscribe("power_model/max_speed")

    # Add static text
    img = Image.new('RGBA', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    draw.text((0, text_height*1), "REC Power:", font=text_font, fill='black')
    draw.text((0, text_height*2), "Power:", font=text_font, fill='black')
    draw.text((0, text_height*3), "Cadence:", font=text_font, fill='black')
    draw.text((0, text_height*4), "Distance:", font=text_font, fill='black')
    draw.text((WIDTH/2 - 300, HEIGHT-speed_height), "SP:", font=speed_font, fill='black')
    draw.text((WIDTH/2 - 300, HEIGHT-speed_height*2), "REC:", font=speed_font, fill='black')
    draw.text((WIDTH/2 - 300, HEIGHT-speed_height*3), "MAX:", font=speed_font, fill='black')

    overlay = camera.add_overlay(img.tobytes(), format='rgba', size=img.size)
    overlay.layer = 3
    overlay.fullscreen = True

def on_message(client, userdata, msg):
    global START_TIME
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    current_time = round(time.time(), 2)
    if msg.topic == "power_model/recommended_SP":
        req_data = str(msg.payload.decode("utf-8"))
        parsed_data = parse_data(req_data)
        REQUIRED_DATA["rec_power"] = float(parsed_data["rec_power"])
        REQUIRED_DATA["rec_speed"] = float(parsed_data["rec_speed"])
    elif msg.topic == "power_model/max_speed":
        max_speed = str(msg.payload.decode("utf-8"))
        REQUIRED_DATA["max_speed"] = float(max_speed)
    elif msg.topic == "data":
        data = str(msg.payload.decode("utf-8"))
        parsed_data = parse_data(data)
        print(str(parsed_data))
        GLOBAL_DATA["power"] += int(parsed_data["power"])
        GLOBAL_DATA["cadence"] += int(parsed_data["cadence"])
        if int(parsed_data["gps"]) == 1:
            GLOBAL_DATA["gps_speed"] += float(parsed_data["gps_speed"])
        GLOBAL_DATA["reed_distance"] += float(parsed_data["reed_distance"])
        GLOBAL_DATA["count"] = GLOBAL_DATA["count"] + 1
        total_time = current_time - START_TIME
        update_time = 0.5
        if total_time >= update_time:
            START_TIME = current_time
            # Create a transparent image to attach text
            img = Image.new('RGBA', (WIDTH, HEIGHT))
            draw = ImageDraw.Draw(img)
            
            # Display power
            if GLOBAL_DATA["power"] != 0:
                power = GLOBAL_DATA["power"]/GLOBAL_DATA["count"]
                rec_power = REQUIRED_DATA["rec_power"]
                tolerance = 0.05
                # Display recommended power
                draw.text((300, text_height*1), "{0}".format(round(rec_power, 2)), font=text_font, fill='black')
                # Display power
                if power> rec_power and power < (rec_power + (rec_power*tolerance)):
                    draw.text((300, text_height*2), "{0}".format(round(power, 2)), font=text_font, fill='green')
                    
                elif power > (rec_power + (rec_power*tolerance)):
                    draw.text((300, text_height*2), "{0}".format(round(power, 2)), font=text_font, fill='red')

                else:
                    draw.text((300, text_height*2), "{0}".format(round(power, 2)), font=text_font, fill='black')

            # Display cadence
            if GLOBAL_DATA["cadence"] != 0:
                cadence = GLOBAL_DATA["cadence"]/GLOBAL_DATA["count"]
                draw.text((300, text_height*3), "{0}".format(round(cadence, 2)), font=text_font, fill='black')

            # Display speed
            if int(parsed_data["gps"]) == 1:
                if GLOBAL_DATA["gps_speed"] != 0:
                    speed_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',speed_height)
                    # Max Speed
                    max_speed = REQUIRED_DATA["max_speed"]
                    max_speed_text = "{0} km/h".format(round(max_speed, 2))
                    draw.text((WIDTH/2 - 70, HEIGHT-speed_height*3), max_speed_text, font=speed_font, fill='black')

                    # Recommended speed
                    rec_speed = REQUIRED_DATA["rec_speed"]
                    rec_speed_text = "{0} km/h".format(round(rec_speed, 2))
                    draw.text((WIDTH/2 - 70, HEIGHT-speed_height*2), rec_speed_text, font=speed_font, fill='black')
                    
                    # Actual speed
                    speed = GLOBAL_DATA["gps_speed"]/GLOBAL_DATA["count"]
                    speed_text = "{0} km/h".format(round(speed, 2))
                    if speed> rec_speed and speed < (rec_speed + (rec_speed*tolerance)):
                        draw.text((WIDTH/2 - 70, HEIGHT-speed_height), speed_text, font=speed_font, fill='green')
                        
                    elif speed > (rec_speed + (rec_speed*tolerance)):
                        draw.text((WIDTH/2 - 70, HEIGHT-speed_height), speed_text, font=speed_font, fill='red')

                    else:
                        draw.text((WIDTH/2 - 70, HEIGHT-speed_height), speed_text, font=speed_font, fill='black')

            # Display reed_distance (distance travelled)
            if GLOBAL_DATA["reed_distance"] != 0:
                reed_distance = GLOBAL_DATA["reed_distance"]/GLOBAL_DATA["count"]
                draw.text((300, text_height*4), "{0}".format(round(reed_distance, 2)), font=text_font, fill='black')
                
                
            # Remove and add the image to the preview overlay
            global PREV_OVERLAY
            if PREV_OVERLAY:
                camera.remove_overlay(PREV_OVERLAY)
            overlay = camera.add_overlay(img.tobytes(), format='rgba', size=img.size)
            overlay.layer = 3
            overlay.fullscreen = True
            PREV_OVERLAY = overlay
            
            # Reset variables
            GLOBAL_DATA["power"] = 0
            GLOBAL_DATA["cadence"] = 0
            GLOBAL_DATA["gps_speed"] = 0
            GLOBAL_DATA["reed_distance"] = 0
            GLOBAL_DATA["count"] = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_log = on_log

client.connect(brokerIP, 1883, 60)

# mqtt loop
# Position and size of the preview window(x,y,width,height)
camera.start_preview(fullscreen=False, window=(0,-20,WIDTH,HEIGHT))
client.loop_forever()

