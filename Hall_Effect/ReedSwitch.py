import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        button_state = GPIO.input(24)
        if button_state == False:
            print "Switch closed."
        else:
            print "Switch open."
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
