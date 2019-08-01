# For speed attempt Data display: time lapsed, zone distance left, recommended power, predicted max speed, max speed, current 
# speed and power.
from picamera import PiCamera, Color
from PIL import Image, ImageDraw, ImageFont
import time
import paho.mqtt.client as mqtt

# Resolution of camera preview
WIDTH = 1280
HEIGHT = 740

bottom_text_height= 70
bottom_text_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',bottom_text_height)
top_text_height = 45
top_text_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',top_text_height)
top_box_height = 80
top_box_width = WIDTH

brokerIP = "192.168.100.100"

PREV_OVERLAY = None
START_TIME = round(time.time(), 2) # static, doesn't change
PREV_TIME = 0 # updated every time on_message() is called
MAX_SPEED = 0

DAS_DATA = {
    "power": 0,
    "cadence": 0,
    "gps_speed": 0,
    "reed_distance": 0,
    "count": 0,
}

POWER_MODEL_DATA = {
    "rec_power": 0,
    "pred_max_speed": 0,
    "zdist": 0,
    "plan_name": ""
}

# Initiate camera preview
camera = PiCamera(resolution=(WIDTH, HEIGHT))

# Calculate max speed
def actual_max(cur_speed):
    global MAX_SPEED
    if cur_speed > MAX_SPEED:
        MAX_SPEED = cur_speed

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
    # Subscribed topics
    client.subscribe("start")
    client.subscribe("data")
    client.subscribe("stop")
    client.subscribe("power_model/recommended_SP")
    client.subscribe("power_model/predicted_max_speed")
    client.subscribe("power_model/plan_name")

    # Add static text
    img = Image.new('RGBA', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0,0),(top_box_width,top_box_height)),fill='black')
    draw.text((0,(top_box_height-top_text_height)/2+8), 'T: ', font=top_text_font, fill='white')
    draw.text((256,(top_box_height-top_text_height)/2+8), 'ZDL: ', font=top_text_font, fill='white')
    draw.text((512,(top_box_height-top_text_height)/2+8), 'RP: ', font=top_text_font, fill='white')
    draw.text((768,(top_box_height-top_text_height)/2+8), 'PMV: ', font=top_text_font, fill='white')
    draw.text((1024,(top_box_height-top_text_height)/2+8), 'MS: ', font=top_text_font, fill='white')
    overlay = camera.add_overlay(img.tobytes(), format='rgba', size=img.size)
    overlay.layer = 3
    overlay.fullscreen = False
    overlay.window = (0, -20, WIDTH, HEIGHT)

def on_message(client, userdata, msg):
    global START_TIME
    global PREV_TIME
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    current_time = round(time.time(), 2)
    if msg.topic == "power_model/recommended_SP":
        req_data = str(msg.payload.decode("utf-8"))
        parsed_data = parse_data(req_data)
        POWER_MODEL_DATA["rec_power"] = int(parsed_data["rec_power"])
        POWER_MODEL_DATA["zdist"] = int(parsed_data["zdist"])
    elif msg.topic == "power_model/predicted_max_speed":
        pred_max_speed = str(msg.payload.decode("utf-8"))
        parsed_data = parse_data(pred_max_speed)
        POWER_MODEL_DATA["pred_max_speed"] = int(parsed_data["predicted_max_speed"])
    elif msg.topic == "power_model/plan_name":
        plan_name = str(msg.payload.decode("utf-8"))
        parsed_data = parse_data(plan_name)
        POWER_MODEL_DATA["plan_name"] = str(parsed_data["plan_name"])
    elif msg.topic == "data":
        data = str(msg.payload.decode("utf-8"))
        parsed_data = parse_data(data)
        print(str(parsed_data))
        DAS_DATA["power"] += int(parsed_data["power"])
        DAS_DATA["cadence"] += int(parsed_data["cadence"])
        if int(parsed_data["gps"]) == 1:
            DAS_DATA["gps_speed"] += float(parsed_data["gps_speed"])
        DAS_DATA["reed_distance"] += float(parsed_data["reed_distance"])
        DAS_DATA["count"] = DAS_DATA["count"] + 1
        if PREV_TIME == 0:
            total_time = current_time - START_TIME
        else:
            total_time = current_time - PREV_TIME
        update_time = 1
        if total_time >= update_time:
            PREV_TIME = current_time
            # Create a transparent image to attach text
            img = Image.new('RGBA', (WIDTH, HEIGHT))
            draw = ImageDraw.Draw(img)

            # Display elapsed time:
            hours, rem = divmod(time.time()-START_TIME, 3600)
            minutes, seconds = divmod(rem, 60)
            draw.text((50,(top_box_height-top_text_height)/2+8), "{:0>2}:{:0>2}".format(int(minutes),int(seconds)), font=top_text_font, fill='white') 

            # Display power
            if DAS_DATA["power"] != 0:
                power = DAS_DATA["power"] / DAS_DATA["count"]
                rec_power = POWER_MODEL_DATA["rec_power"]
                # Display recommended power
                draw.text((600, (top_box_height-top_text_height)/2+8), "{0}".format(round(rec_power, 0)), font=top_text_font, fill='white')
                # Display power (no colour change)
                draw.text((WIDTH/2-90, HEIGHT-bottom_text_height), "P:{0}".format(round(power,2)), font=bottom_text_font, fill='red')

            # Display speed
            if int(parsed_data["gps"]) == 1:
                if DAS_DATA["gps_speed"] != 0:
                    # Predicted max speed
                    pred_max_speed = POWER_MODEL_DATA["pred_max_speed"]
                    draw.text((890, (top_box_height-top_text_height)/2+8), "{0}".format(round(pred_max_speed,2)), font=top_text_font, fill='white')

                    # Actual speed (no colour change)
                    speed = DAS_DATA["gps_speed"] / DAS_DATA["count"]
                    speed_text = "{0}".format(round(speed, 2))
                    draw.text((WIDTH/2-90, HEIGHT-bottom_text_height*2-30), "S:{0}".format(round(speed,2)), font=bottom_text_font,fill='red')

                    # Actual max speed
                    actual_max(speed)
                    draw.text((1120, (top_box_height-top_text_height)/2+8), "{0}".format(int(MAX_SPEED)), font = top_text_font, fill='white')

            # Display zone distance left (bugged)
            if POWER_MODEL_DATA["zdist"] != 0:
                zdist_left = POWER_MODEL_DATA["zdist"]
                draw.text((360,(top_box_height-top_text_height)/2+8), "{0}".format(int(zdist_left)), font=top_text_font, fill='white')

            # Display plan name and clear after 15 secs
            if POWER_MODEL_DATA["plan_name"] != '' and time.time()-START_TIME <= 15:
                plan_name = POWER_MODEL_DATA["plan_name"]
                draw.text((0, HEIGHT-top_text_height),"{}".format(plan_name), font=top_text_font, fill='red')

            # Remove and add the image to the preview overlay
            global PREV_OVERLAY
            if PREV_OVERLAY:
                camera.remove_overlay(PREV_OVERLAY)
            overlay = camera.add_overlay(img.tobytes(), format='rgba', size=img.size)
            overlay.layer = 3
            overlay.fullscreen = False
            overlay.window = (0,-20, WIDTH, HEIGHT)
            PREV_OVERLAY = overlay
            
            # Reset variables
            DAS_DATA["power"] = 0
            DAS_DATA["cadence"] = 0
            DAS_DATA["gps_speed"] = 0
            DAS_DATA["reed_distance"] = 0
            DAS_DATA["count"] = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_log = on_log

client.connect_async(brokerIP, 1883, 60)

# mqtt loop
# Position and size of the preview window(x,y,width,height)
camera.start_preview(fullscreen=False, window=(0,-20,WIDTH,HEIGHT))
client.loop_start()
while True:
    time.sleep(1)


