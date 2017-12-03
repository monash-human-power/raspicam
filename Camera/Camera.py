# Test Overlay Timer - has three overlays
import picamera
import time
from PIL import Image, ImageDraw, ImageFont
import os

# Video Resolution
VIDEO_HEIGHT = 480
VIDEO_WIDTH = 800

font = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 20)
fontBold = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 20)

textPad = Image.new('RGB', (512, 64))
textPadImage = textPad.copy()

textPad2 = Image.new('RGB', (128, 64), "#298")
textPadImage2 = textPad2.copy()

j = 0
while os.path.exists("/home/pi/Documents/MHP_raspicam/Camera/Video/Recording_%s.h264" % j):
    j += 1

#filename = "video" + str(j) + + ".h264"
filename = "/home/pi/Documents/MHP_raspicam/Camera/Video/Recording_%s.h264" % j

i = 0
with picamera.PiCamera() as camera:
    camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
    camera.vflip = True
    camera.framerate = 45
    camera.led = True
    camera.start_preview()
    camera.start_recording(filename)
    camera.wait_recording(0.9)

# Layer 3 overlay
    overlay = camera.add_overlay(textPadImage.tobytes(), size=(
        512, 64), alpha=128, layer=3, fullscreen=False, window=(0, 20, 512, 64))
    textPadImage = textPad.copy()
    drawTextImage = ImageDraw.Draw(textPadImage)
    drawTextImage.text((75, 18), "SECONDARY", font=fontBold, fill=("Red"))
    overlay.update(textPadImage.tobytes())

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

        camera.stop_preview()

        print ("\nCancelled")

    finally:

        camera.stop_recording()
        camera.stop_preview()

print("end test")
