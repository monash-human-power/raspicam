# ---------------------------------------------------------------------
# Last Modified:
#   30-12-2017
# Description:
#   This program is the test master. It decides which modules run append
#   and in what order.
# ---------------------------------------------------------------------

import subprocess
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

recording = 0
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("")
try:
    while True:
        print("Ready!\n")
        while True:
            button_state = GPIO.input(24)
            if button_state == False:
                print("Starting Data Recording v2a...")
                recording = 1
                break
            sleep(0.2)

        subprocess.call(["python", "send.py"])
        sleep(1)
        print("Recording!\n")

        while True:
            button_state = GPIO.input(24)
            if button_state == False:
                print("Stopping Data Recording v2a...")
                subprocess.call(["python", "send.py"])
                recording = 0
                print("Waiting.....\n\n")
                sleep(3)
                break
except KeyboardInterrupt:
    if recording == 1:
        print("\n\nStopping Data Recording v2a...\n")
        subprocess.call(["python", "send.py"])
        print("Program Ended.\n")
    else:
        print("\n\nProgram Ended.\n")
    GPIO.cleanup()
