#!/bin/sh

now=$(date +"RUN_%d_%m_@_%H-%M-%S")

#ffmpeg -r 45 -i /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_$1.h264 -vcodec copy /home/pi/Documents/MHP_raspicam/Camera/Video/$now.mkv

# Primary
ffmpeg -r 45 -i /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_0.h264 -vcodec copy /media/pi/7A49-A5AB/$now.mkv

# Secondary
ffmpeg -r 45 -i /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_0.h264 -vcodec copy /media/pi/C83F-EC3A/$now.mkv

sudo rm /home/pi/Documents/MHP_raspicam/Camera/Video/*.h264
