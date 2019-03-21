import RPi.GPIO as gpio
from time import sleep
import subprocess

gpio.setmode(gpio.BOARD)
gpio.setup(15, gpio.IN, pull_up_down=gpio.PUD_UP)

try:
    #while True:
    while True:
    """
    if switch_state == False:
                    print("Close")
                else:
                    print("Open")
                """
        switch_state = gpio.input(15)
        if switch_state:
            print("HIGH")
        else:
            print("LOW")
            break
        p1 = subprocess.Popen(["python", "/home/pi/Documents/MHP_Raspicam/Documentation/Development_Code/StartCamera.py"])
        sleep(1)
        """
        while True:
            switch_state = gpio.input(15)
            if switch_state:
                print("HIGH")
                subprocess.Popen.kill(p1)
                break
            else:
                print("LOW")
            sleep(1)
        """
except KeyboardInterrupt:
    gpio.cleanup()
