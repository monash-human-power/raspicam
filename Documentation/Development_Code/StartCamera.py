from picamera import PiCamera
from time import sleep

WIDTH = 800
HEIGHT = 480

camera = PiCamera(resolution=(WIDTH, HEIGHT))
camera.start_preview()

