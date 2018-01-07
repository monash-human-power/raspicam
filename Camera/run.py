import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        while True:
            button_state = GPIO.input(24)
            if button_state == False:
                print("\nStarting Camera Recording..")
                break
            time.sleep(0.2)

        p1 = subprocess.Popen(["python", "Camera.py"])
        sleep(1)

        while True:
            button_state = GPIO.input(24)
            if button_state == False:
                p1.terminate()
                print("\n\nExecution Terminated.\n")
                break
            time.sleep(0.2)
except KeyboardInterrupt:
    p1.terminate()
    print("\n\nProgram Ended.\n")
    GPIO.cleanup()
