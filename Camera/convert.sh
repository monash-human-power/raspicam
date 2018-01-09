#!/bin/sh

ffmpeg -r 45 -i /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_$1.h264 -vcodec copy /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_$1.mkv
