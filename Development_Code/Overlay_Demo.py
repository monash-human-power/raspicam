# Written by: Minh T Nguyen
# Last modified: 16/7/2018
# Softwares: Python 3.4.2, picamera 1.13, PIL 1.1.7
# Hardwares: Camera Module V2.1, Official 7" touchscreen monitor

# Descriptions:

from picamera import PiCamera, Color
from PIL import Image, ImageDraw, ImageFont
from time import sleep
import datetime as dt

# Current system using 800x480
WIDTH = 800
HEIGHT = 480

# Initiate camera preview
camera = PiCamera(resolution=(WIDTH, HEIGHT))
camera.start_preview()

# Create a transparent image to attach text
img = Image.new('RGBA', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

# Text display for speed
number_height = 50
unit_height = 25
number_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',number_height)
unit_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',unit_height)
number = '{}'.format(0.0)
unit = ' km/h'
draw.text((WIDTH/2 - 65, HEIGHT-number_height+2), number, font=number_font, fill='black')
draw.text((WIDTH/2, HEIGHT-unit_height), unit, font=unit_font, fill='black')

# Text display for power, cadence (pedalling rate), distance, heart rate
# *CODE FOR DEMO ONLY*
display_text = ['Pwr: {} W'.format(0),'Cad: {} rpm'.format(0.0), 'Dist: {} km'.format(0.0), 'Heart rate: {} bpm'.format(0)]
text_height = 20
text_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',text_height)
for i in range(len(display_text)):
    draw.text((10, 10 + text_height*i), display_text[i], font=text_font, fill='black')


# Add the image to the preview overlay
overlay = camera.add_overlay(img.tostring(), format='rgba', size=img.size)
overlay.layer = 3
overlay.fullscreen = True

# Text display for time using "annotate_text"
camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
camera.annotate_text_size = 26
camera.annotate_foreground = Color('black')

while True:
    sleep(1)
    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
