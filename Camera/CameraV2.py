#Specifying Imports
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from PIL import Image, ImageDraw, ImageFont
import os

#Camera Setup
camera = PiCamera()

#Pin Setups
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Variable setups
global count 
count = 0
global j
j = 0
global filename 
filename = "video%s.h264" % j

#Overlay Setups
font = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 20) 
fontBold = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 20)
textPad = Image.new('RGB', (512, 64))
textPadImage = textPad.copy()

textPad2 = Image.new('RGB', (128, 64), "#298")
textPadImage2 = textPad2.copy()

#FUNCTIONS
#==============================================
def debouncer_Counter(count):
    time.sleep(0.3)
    if (count == 1):
        count = 0
        camera_Stop()
    else:
        count = 1
        camera_Start()
    #print (count)
    return count

def camera_Start():
    camera.resolution = (800, 480)
    camera.framerate = 45
    camera.start_preview()
    camera.start_recording(filename)
    camera.wait_recording(0.9)

    global overlay
    overlay = camera.add_overlay(textPadImage.tobytes(), size=(512, 64), alpha = 128, layer = 3, fullscreen = False, window = (0,20,512,64))
    global textPadImage 
    textPadImage = textPad.copy()
    drawTextImage = ImageDraw.Draw(textPadImage)
    drawTextImage.text((75, 18),"SECONDARY" , font=fontBold, fill=("Red"))
    overlay.update(textPadImage.tobytes())

def camera_Stop():
    camera.wait_recording(0.9)
    camera.stop_recording()
    camera.stop_preview()
    camera.remove_overlay(overlay)


#==============================================        
#MAIN LOOP 
try:
    while True:
        #Filename setups
        while os.path.exists("video%s.h264" % j):
            j += 1
            filename = "video%s.h264" % j
            
        if(GPIO.input(11) == 0):
            count = debouncer_Counter(count)

        if(count):
            text = "HI"
            global overlay1
            overlay1 = camera.add_overlay(textPadImage2.tobytes(), size=(128, 64), alpha = 128, layer = 4, fullscreen = False, window = (512,20,128,64))
            camera.remove_overlay(overlay2)
except KeyboardInterrupt:
    camera_Stop()



