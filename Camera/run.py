# ---------------------------------------------------------------------
# Last Modified:
#   8-1-2018
# Description:
#   This program is the camera master. It responds to a pushbutton input
#   to start and stop camera recording.
# ---------------------------------------------------------------------

import subprocess
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        while True:
            button_state = GPIO.input(24)
            if button_state == False:
                print("\nStarting Camera Recording...")
                recording = 1
                break
            sleep(0.2)

        p1 = subprocess.Popen(["python", "Camera.py"])
        sleep(1)

        while True:
            button_state = GPIO.input(24)
            if button_state == False:
                print("\n\nStopping Camera Recording...\n")
                subprocess.Popen.kill(p1)
                recording = 0
                time.sleep(3)
                break
            sleep(0.2)
except KeyboardInterrupt:
    if recording == 1:
        subprocess.Popen.kill(p1)
    print("\n\nProgram Ended.\n")
    GPIO.cleanup()
