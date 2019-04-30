import RPi.GPIO as gpio
from time import sleep

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
    turn_on(red_led)
    turn_off(green_led)
    while True:
        switch_state = gpio.input(switch)
        if switch_state:
            print("HIGH")
            turn_on(red_led)
            turn_off(green_led)
        else:
            print("LOW")
            turn_on(green_led)
            turn_off(red_led)
        sleep(0.5)
except KeyboardInterrupt:
    gpio.cleanup()



    
