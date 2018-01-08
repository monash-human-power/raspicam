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

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        button_state = GPIO.input(24)
        if button_state == False:
            print("\nStarting Data Recording v2a...")
            recording = 1
            break
        sleep(0.2)

    p1 = subprocess.Popen(["python", "datav2a.py"])
    sleep(1)

    while True:
        button_state = GPIO.input(24)
        if button_state == False:
            print("\n\nStopping Data Recording v2a...\n")
            subprocess.Popen.kill(p1)
            recording = 0
            p3 = subprocess.call(
                '/home/pi/Documents/MHP_raspicam/Accelerometers/LSM9DS1/BumpTest_Code/Shell_Scripts/sendcsv.sh')
            sleep(3)
            break
except KeyboardInterrupt:
    if recording == 1:
        subprocess.Popen.kill(p1)
    print("\n\nProgram Ended.\n")
    GPIO.cleanup()
