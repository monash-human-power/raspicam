# Description: This file handles the camera module interfacing. It generates the video feed on the screen and also generates an overlay which displays the time on the screen.
# The overlay in this file reads data from a reed switch to calculate speed. Make sure you have the reed switch on the wheel and the wiring hooked up to the display.
# Please note this repo needs to be cloned into the Documents directory on the pi otherwise it will not work.
# Last Modified: Sunday 1st July 2018 by Pat Graham
# Written By: Pat Graham

# This file makes use of pigpio to handle the gpio pins. The reason for this is sampling needs to take place at high speed. To set up pigpio on a new pi
# 1) Navigate to Other_Code/PIGPIO in this repo
# 2) Run "make -j4"
# 3) Run "sudo make install"
# 4) Open the /etc/rc.local file and place the command "sudo pigpiod" before the line "exit 0"
# 5) Reboot the pi

# Import relevant libraries
import picamera			# For setting up camera object
import pigpio			# For handling reed switch input
import time			# For calculating times between reed switch triggers
import os			# For determining filenames
import csv			# For storing reed switch data into a csv file

record = 1	# Global variable to control whether or not data and camera video are recorded or not
pin = 4		# Pin for the reed switch
Pi = 3.14159	# Definition of the irrational number pi for calculating circumference of the wheel
d = 0.5		# Global variable to define the diameter of the wheel.

# Configure reed switch pin as an input with an internal pull up resistor
pi = pigpio.pi()
pi.set_mode(pin, pigpio.INPUT)
pi.set_pull_up_down(4, pigpio.PUD_UP)

# Exit script if there is an issue in the previous step
if not pi.connected:
    exit()

# Set up Camera object
with picamera.PiCamera() as camera:
    camera.resolution = (800, 480)
    camera.framerate = 45
    camera.start_preview()
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = '{}'.format(0.0)

    # Has the user specified to record video and data? If so set this up
    if record == 1:
        # Set up Camera File
        j = 0
        while os.path.exists("/home/pi/Documents/MHP_Raspicam/Video/Recording_%s.h264" % j):
            j += 1
        filename_camera = "/home/pi/Documents/MHP_Raspicam/Video/Recording_%s.h264" % j
        camera.start_recording(filename_camera)

        # Set up Velocity file
        i = 0
        while os.path.exists("/home/pi/Documents/MHP_Raspicam/ReedSwitch/Recording_%s.csv" % i):
            i += 1
        filename_velocity = "/home/pi/Documents/MHP_Raspicam/ReedSwitch/Recording_%s.csv" % i

    # Initialize loop variables
    previous = pi.read(pin)
    prev_time = time.time()
    start_time = time.time()

    # Infinite loop to generate speed overlay
    try:
        while True:

            # Find the next pin read
            next = pi.read(pin)

            # Only trigger when a falling edge is detected
            if next != previous and next == 0:
                next_time = time.time() 				# get the time at this instant
                time_delta = float(next_time - prev_time) 		# calculate time delta
                speed = (1.0 / time_delta) * Pi * d * 3.6 		# determine the speed using distance/time
                camera.annotate_text = '{}'.format(round(speed, 1))	# Put this on the screen

                # Has the user specified to record data? If so write this to a file
                if record == 1:
                    with open(filename_velocity, 'a') as csvfile:
                        filewriter = csv.writer(csvfile)
                        filewriter.writerow(
                            ["%.5f" % (next_time - start_time), "%.2f" % speed, "\n"])

                # Refresh the previous time
                prev_time = next_time

            # Has nothing happened in the last three seconds? The bike has probably stopped and velocity is now zero.
            if (time.time() - prev_time) > 3:
                camera.annotate_text = '{}'.format(0.0)

            # Refresh previous reed switch pin value before next loop
            previous = next

        # End while loop here, repeat

    except KeyboardInterrupt:

        # Handle exception if the user presses control c.
        if record == 1:
            camera.stop_recording()
