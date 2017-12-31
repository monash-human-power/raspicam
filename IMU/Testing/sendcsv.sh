#!/bin/sh

printf "Sending data csv file....\n\n"
time=$(date +%H-%M-%S)
scp /home/pi/Documents/MHP_raspicam/IMU/Testing/Test_Data/Pi_Back.csv pi@patpi.local:/home/pi/Documents/MHP_raspicam/IMU/Testing/Received_Data/pz2_$time.csv
printf "\nData sent.\n\n"

exit 0