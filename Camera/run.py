import subprocess
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        while True:
            button_state = GPIO.input(24)
            if button_state == False:
                print("\nStarting Camera Recording..")
                recording = 1
                break
            time.sleep(0.2)

        p1 = subprocess.Popen(["python", "Camera.py"])
        time.sleep(1)

        while True:
            button_state = GPIO.input(24)
            if button_state == False:
                subprocess.Popen.kill(p1)
                recording = 0
                print("\n\nStopping Camera Recording...\n")
                time.sleep(3)
                break
            time.sleep(0.2)
except KeyboardInterrupt:
    if recording == 1:
        subprocess.Popen.kill(p1)
    print("\n\nProgram Ended.\n")
    GPIO.cleanup()
