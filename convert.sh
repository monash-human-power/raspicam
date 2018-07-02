#!/bin/sh

# Description: This bash script uses a command line utility called fmmpeg to convert camera recording files to .mkv format and store this output on a usb.
# This script deletes all .h264 files of the local sd card at the end of the run to make sure the SD card doesn't fill up.
# Converted files are added to a usb called PRIMARY or SECONDARY and are time and date stamped at the time of conversion.
# Last Modified: Sunday 1st July 2018 by Pat Graham
# Written By: Pat Graham

# You may have to set up ffmpeg on a new pi. To do this
# 1) Run sudo apt-get update
# 2) Run sudo apt-get install ffmpeg

# Get the current date and time
now=$(date +"RUN_%d_%m_@_%H-%M-%S")

<<<<<<< HEAD
# If the display is the primary run this command. This command will fail if the display is the secondary or no usb is plugged in.
ffmpeg -r 45 -i /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_0.h264 -vcodec copy /media/pi/PRIMARY/$now.mkv

# If the display is the secondary run this command. This command will fail if the display is the primary or no usb is plugged in.
ffmpeg -r 45 -i /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_0.h264 -vcodec copy /media/pi/SECONDARY/$now.mkv

# Remove .h264 files from the SD Card
sudo rm /home/pi/Documents/MHP_Raspicam/Video/*.h264
=======
# Primary
ffmpeg -r 45 -i /home/pi/Documents/MHP_Raspicam/Video/Recording_0.h264 -vcodec copy /media/pi/PRIMARY/$now.mkv

# Secondary
ffmpeg -r 45 -i /home/pi/Documents/MHP_Raspicam/Video/Recording_0.h264 -vcodec copy /media/pi/SECONDARY/$now.mkv

sudo rm /home/pi/Documents/MHP_Raspicam/Video/*.h264
>>>>>>> dbf10f4f776629d6afcc24f529c47f4f328739bc
