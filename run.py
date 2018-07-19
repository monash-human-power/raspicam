# Description: This file indicates the current status of the camera system. It is designed to be run on boot and controls configuration of the whole system.
# The script is controlled by one push button. When this is pressed it starts a Camera script as specified by global variables. It constantly updates some LEDs so that
# external users are aware of the status of the system.
# Last Modified: Sunday 1st July 2018 by Pat Graham
# Written By: Pat Graham

# ---------------------------------------------------------------------
# Last Modified:
#   8-1-2018
# Description:
#   This program is the camera master. It responds to a pushbutton input
#   to start and stop camera recording.
# ---------------------------------------------------------------------

import subprocess
import RPi.GPIO as GPIO
from time import sleep

# Some notes
# 1) If the script is running the LEDs will light up. If they are not lit up, start the script
# 2) If this script thinks the camera system is running, it will turn off the red LED and turn on the green LED. If no camera feed is seen on the screen
#    then most likely there is an error in the wiring somewhere. Check to make sure the ribbon cable is connected properly and that the camera module is
#    enabled in "sudo raspi-config" interfacing sub-menu.

# Import relevant libraries
import subprocess		# For passing of handling of Camera feed to subprocesses
import RPi.GPIO as GPIO		# For monitoring the state of the push button and updating status LEDs
from time import sleep		# For allowing the script to pause occasionally

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Global variables to define configuration of the system
convert = True		# does the user want to convert the files and have them removed from the SD card? If no usb is connected this simply deletes each file after it is recorded.
rec_num = 0		# Keep track of the number of recordings
velocity = 1;		# Does the user want to run Camera.py or CameraVel.py? CamerVel.py is run when this variable is 1.
recording = 1		# Global variable to indicate the status of the sytem
convert = True # Control whether or not you convert the .h264 file to a .mkv file
rec_num = 0 # Changes the starting recording number in the Videos sub-folder
velocity = 1 # change this variable to change wether Camera.py or CameraVel.py is run
recording = 1 # global flag that tells the script the pi's current recording status

# Set up GPIO Pins
GPIO.setup(22,GPIO.OUT) 				# Green LED
GPIO.setup(23,GPIO.OUT) 				# Red LED
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Push button (input with internal pull up resistor)

# Start Main loop
try:

    # For neatness of printing when run from command line
    print("")

    # Update status LEDs. Turn Red LED on, Green LED off. System inactive.
    GPIO.output(22,GPIO.LOW)
    GPIO.output(23,GPIO.HIGH)

    # Start infinite while loop
    while True:

        # Indicate the system is read to record on the command line
        print("Ready!\n")


        # Loop here until the push button is pressed. Active low.
        while True:

            # Read push button
            button_state = GPIO.input(25)

            # Has it been pressed? If yes enter this section
            if button_state == False:
                print("Starting Camera Recording...\n")		# Recognise input on command line
                recording = 1					# Update global status variable
                GPIO.output(22,GPIO.HIGH)			# Turn RED LED off
                GPIO.output(23,GPIO.LOW)			# Turn Green LED on
                break						# Break out of infinite while loop to progress to next step

            # If no then wait a little bit before reading again.
            sleep(0.2)

        # Has the user specified CameraVel.py or Camera.py? Open the specified Camera script.
	if velocity == 1:
            p1 = subprocess.Popen(["python", "/home/pi/Documents/MHP_Raspicam/CameraVel.py"])
        else:
	    p1 = subprocess.Popen(["python", "/home/pi/Documents/MHP_Raspicam/Camera.py"])
	sleep(1)

        # Now loop here until the push button is pressed to close off camera recording.
        while True:

            # Read the push button
            button_state = GPIO.input(25)

            # Has the push button been pressed? If yes enter this section
            if button_state == False:
                print("\nStopping Camera Recording...\n\n")	# Recognise input on command line
                subprocess.Popen.kill(p1)			# Kill Camera script
                recording = 0					# Update global variable

                # Did the user specify they wanted files converted and then delete from SD card? Do this now.
                if convert == True:
                    subprocess.call(["bash", "/home/pi/Documents/MHP_Raspicam/convert.sh", str(rec_num)])
                    rec_num = rec_num + 1	# Update recording number
                    rec_num = rec_num + 1
                    print("")

                # Wait a little bit for conversion to complete. Depending on the size of the file this delay may have to be increased.
                print("Wait....\n")
                sleep(1)

                # Update status LEDs
                GPIO.output(22,GPIO.LOW)
                GPIO.output(23,GPIO.HIGH)

                # Exit infinite loop. Proceed back to monitor push button for start of camera system.
                break

            # No button pressed? Sleep for a little bit before next read.
            sleep(0.2)

except KeyboardInterrupt:

    # If User presses control c on command line and camera is recording, stop camera recording
    if recording == 1:
        subprocess.Popen.kill(p1)
    print("\n\nProgram Ended.\n")
    GPIO.cleanup()
