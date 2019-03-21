import RPi.GPIO as gpio
from time import sleep
import subprocess

# Pins
switch = 15
green_led = 11
red_led = 13

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

gpio.setup(switch, gpio.IN, pull_up_down=gpio.PUD_UP)   #toggle switch
gpio.setup(green_led, gpio.OUT)    #green LED
gpio.setup(red_led, gpio.OUT)

def turn_on(led):
    gpio.output(led,gpio.HIGH)


def turn_off(led):
    gpio.output(led,gpio.LOW)
    
try:
    while True:
        while True:
            turn_on(red_led)
            switch_state = gpio.input(15)
            if switch_state:
                print("OFF")
            else:
                print("ON")
                break
            sleep(0.5)
        # TODO: Remove hard coding of directory of python script
        p1 = subprocess.Popen(["python", "/home/pi/Documents/MHP_Raspicam/Documentation/Development_Code/StartCamera.py"])
        turn_off(red_led)
        turn_on(green_led)
        sleep(1)
        
        while True:
            switch_state = gpio.input(15)
            if switch_state:
                print("OFF")
                subprocess.Popen.kill(p1)
                turn_off(green_led)
                break
            else:
                print("ON")
            sleep(1)
        
except KeyboardInterrupt:
    subprocess.Popen.kill(p1)
    gpio.cleanup()
