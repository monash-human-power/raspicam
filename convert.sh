#!/bin/sh

now=$(date +"RUN_%d_%m_@_%H-%M-%S")

#ffmpeg -r 45 -i /home/pi/Documents/MHP_raspicam/Camera/Video/Recording_$1.h264 -vcodec copy /home/pi/Documents/MHP_raspicam/Camera/Video/$now.mkv

# Primary
ffmpeg -r 45 -i /home/pi/Documents/MHP_Raspicam/Video/Recording_0.h264 -vcodec copy /media/pi/PRIMARY/$now.mkv

# Secondary
ffmpeg -r 45 -i /home/pi/Documents/MHP_Raspicam/Video/Recording_0.h264 -vcodec copy /media/pi/SECONDARY/$now.mkv

sudo rm /home/pi/Documents/MHP_Raspicam/Video/*.h264