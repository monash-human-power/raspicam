#!/bin/sh

printf "\nSending data csv file....\n\n"
scp /home/pi/Documents/MHP_raspicam/IMU/Testing/Test_Data/Pi_Back.csv pi@patpi.local:/home/pi/Documents/Received_Data/Pi_Zero_2.csv
printf "\nData sent.\n\n"
