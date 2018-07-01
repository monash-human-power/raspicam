# Description: This file handles the camera module interfacing. It generates the video feed on the screen and also generates an overlay which displays the time on the screen.
# There are three overlays in this file. In order to smooth transistions two are rotated constantly so that the time can be update at each second.
# Please note this repo needs to be cloned into the Documents directory on the pi otherwise it will not work.
# Last Modified: Sunday 1st July 2018 by Pat Graham
# Written By: MyPiDrone (https://github.com/MyPiDrone/MyPiModule/blob/master/MyPiCamera_sample5.py)

# Import relevant libraries
import picamera						# For generating a camera object
import socket 						# For hostname detection
import time 						# For displaying the time
from PIL import Image, ImageDraw, ImageFont		# For generating camera overlay
import os						# For detecting existing files
from time import sleep					# For pausing the script

# Video Resolution
VIDEO_HEIGHT = 480	# Video height in pixels
VIDEO_WIDTH = 800	# Video width in pixels

# Specific font used by the overlay. This may not be installed on a pi at first instance. Run "sudo apt-get install fonts-roboto" to install.
font = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 20)
fontBold = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 20)

# Create textpads for overlay
textPad = Image.new('RGB', (512, 64))
textPadImage = textPad.copy()

textPad2 = Image.new('RGB', (128, 64), "#298")
textPadImage2 = textPad2.copy()

# Check out which files already exist, generate a video filename based of this.
j = 0
while os.path.exists("/home/pi/Documents/MHP_Raspicam/Video/Recording_%s.h264" % j):
    j += 1

filename = "/home/pi/Documents/MHP_Raspicam/Video/Recording_%s.h264" % j

# Variable to help idenitfy which of the two overlays is active
i = 0

# Set up Camera object
with picamera.PiCamera() as camera:
    camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
    if socket.gethostname() == "Secondary":
        camera.vflip = True
    camera.framerate = 45
    camera.led = True
    camera.start_preview()
    camera.start_recording(filename)
    camera.wait_recording(0.9)

    # Put first overlay on. This is the Layer 3 overlay.
    overlay = camera.add_overlay(textPadImage.tobytes(), size=(
        512, 64), alpha=128, layer=3, fullscreen=False, window=(0, 20, 512, 64))
    textPadImage = textPad.copy()
    drawTextImage = ImageDraw.Draw(textPadImage)
    if socket.gethostname() == "Secondary":
        drawTextImage.text((75, 18), "SECONDARY", font=fontBold, fill=("Red"))
    else
        drawTextImage.text((75, 18), "PRIMARY", font=fontBold, fill=("Red"))
    overlay.update(textPadImage.tobytes())

    # Now loop infinitely updating the time at one second intervals. Rotate overlays so transisitons are smooth.
    try:
        while True:

            # Layer 4 overlay
            text = time.strftime('%H:%M:%S', time.localtime())
            overlay1 = camera.add_overlay(textPadImage2.tobytes(), size=(
                128, 64), alpha=128, layer=4, fullscreen=False, window=(512, 20, 128, 64))
            textPadImage2 = textPad2.copy()
            drawTextImage = ImageDraw.Draw(textPadImage2)
            drawTextImage.text((22, 20), text, font=font, fill=("black"))
            overlay1.update(textPadImage2.tobytes())
            if i == 0:
                i = 1
            else:
                camera.remove_overlay(overlay2)
            camera.wait_recording(0.9)

            # Layer 5 overlay
            text = time.strftime('%H:%M:%S', time.localtime())
            overlay2 = camera.add_overlay(textPadImage2.tobytes(), size=(
                128, 64), alpha=128, layer=5, fullscreen=False, window=(512, 20, 128, 64))
            textPadImage2 = textPad2.copy()
            drawTextImage = ImageDraw.Draw(textPadImage2)
            drawTextImage.text((22, 20), text, font=font, fill=("black"))
            overlay2.update(textPadImage2.tobytes())
            camera.remove_overlay(overlay1)
            camera.wait_recording(0.9)

    except KeyboardInterrupt:

        # End script if Ctrl C is pressed
        camera.stop_preview()
        print ("\nCancelled")

    finally:

        # When exiting gracefully close off camera recording
        camera.stop_recording()
        camera.stop_preview()

print("end test")
