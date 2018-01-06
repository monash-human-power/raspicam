#!/bin/sh


printf "\nSending data csv file....\n\n"
time=$(date +%H-%M-%S)
scp /home/pi/Documents/MHP_raspicam/Accelerometers/LSM9DS1/BumpTest_Code/Pi_Data_v2a.csv pi@patpi.local:/home/pi/Documents/MHP_raspicam/Accelerometers/LSM9DS1/BumpTest_Code/Received_Data/pz3_$time.csv
printf "\nData sent.\n\n"
