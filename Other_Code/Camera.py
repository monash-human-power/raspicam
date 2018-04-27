# Test Overlay Timer - has three overlays
import picamera
import time
import pigpio
from PIL import Image, ImageDraw, ImageFont
import os

record = 1
pin = 4
Pi = 3.14159
d = 0.5

pi = pigpio.pi()
pi.set_mode(pin, pigpio.INPUT)
pi.set_pull_up_down(pin, pigpio.PUD_UP)

font = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 20)
fontBold = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 20)
textPad = Image.new('RGB', (512, 64))
textPadImage = textPad.copy()
textPad2 = Image.new('RGB', (128, 64), "#298")
textPadImage2 = textPad2.copy()

if not pi.connected:
    exit()

with picamera.PiCamera() as camera:
    camera.resolution = (800, 480)
    camera.vflip = False
    camera.framerate = 45
    camera.start_preview()

    overlay = camera.add_overlay(textPadImage.tobytes(), size=(
        512, 64), alpha=128, layer=3, fullscreen=False, window=(0, 20, 512, 64))
    textPadImage = textPad.copy()
    drawTextImage = ImageDraw.Draw(textPadImage)
    drawTextImage.text((75, 18), "PRIMARY", font=fontBold, fill=("Red"))
    overlay.update(textPadImage.tobytes())

    if record == 1:
        j = 0
        while os.path.exists("/home/pi/Documents/MHP_Raspicam/Video/Recording_%s.h264" % j):
            j += 1
        filename = "/home/pi/Documents/MHP_Raspicam/Video/Recording_%s.h264" % j
        camera.start_recording(filename)

    previous = pi.read(pin)
    prev_time = time.time()

    try:
        while True:

            next = pi.read(pin)

            if next != previous and next == 0:
                next_time = time.time()
                time_delta = float(next_time - prev_time)
                speed = (1.0 / time_delta) * Pi * d * 3.6

                if i == 0:
                    text = '{}'.format(round(speed, 1))
                    overlay1 = camera.add_overlay(textPadImage2.tobytes(), size=(
                        128, 64), alpha=128, layer=4, fullscreen=False, window=(512, 20, 128, 64))
                        textPadImage2 = textPad2.copy()
                        drawTextImage = ImageDraw.Draw(textPadImage2)
                        drawTextImage.text((22, 20), text, font=font, fill=("black"))
                        overlay1.update(textPadImage2.tobytes())
                        i = 1

                if i == 1:
                    text = time.strftime(round(speed, 1))
                    overlay2 = camera.add_overlay(textPadImage2.tobytes(), size=(
                        128, 64), alpha=128, layer=5, fullscreen=False, window=(512, 20, 128, 64))
                    textPadImage2 = textPad2.copy()
                    drawTextImage = ImageDraw.Draw(textPadImage2)
                    drawTextImage.text((22, 20), text, font=font, fill=("black"))
                    overlay2.update(textPadImage2.tobytes())
                    camera.remove_overlay(overlay1)
                    i = 0

                prev_time = next_time

            if (time.time() - prev_time) > 3:
                if i == 0:
                    text = '{}'.format(round(speed, 1))
                    overlay1 = camera.add_overlay(textPadImage2.tobytes(), size=(
                        128, 64), alpha=128, layer=4, fullscreen=False, window=(512, 20, 128, 64))
                    textPadImage2 = textPad2.copy()
                    drawTextImage = ImageDraw.Draw(textPadImage2)
                    drawTextImage.text((22, 20), text, font=font, fill=("black"))
                    overlay1.update(textPadImage2.tobytes())
                    i = 1

                if i == 1:
                    text = time.strftime(round(speed, 1))
                    overlay2 = camera.add_overlay(textPadImage2.tobytes(), size=(
                        128, 64), alpha=128, layer=5, fullscreen=False, window=(512, 20, 128, 64))
                    textPadImage2 = textPad2.copy()
                    drawTextImage = ImageDraw.Draw(textPadImage2)
                    drawTextImage.text((22, 20), text, font=font, fill=("black"))
                    overlay2.update(textPadImage2.tobytes())
                    camera.remove_overlay(overlay1)
                    i = 0

#	    if record == 1:
#		camera.wait_recording(0.2)

            previous = next

    except KeyboardInterrupt:
        if record == 1:
            camera.stop_recording()
