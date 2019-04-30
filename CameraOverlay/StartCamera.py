from picamera import PiCamera
from time import sleep

WIDTH = 800
HEIGHT = 480

with PiCamera() as camera:
    camera.resolution = (WIDTH, HEIGHT)
    camera.framerate = 45
    camera.start_preview()
    while True:
        pass
    
    
