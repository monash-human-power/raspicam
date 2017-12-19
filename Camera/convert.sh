#!/bin/sh

#ffmpeg -r 45 -i /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_$1.h264 -vcodec copy /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_$1.mkv

ffmpeg -r 45 -i /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_0.h264 -vcodec copy /media/pi/7A49-A5AB/Recording_$1.mkv

sudo rm /home/pi/Documents/MHP_raspicam/Camera/Video/*.h264
