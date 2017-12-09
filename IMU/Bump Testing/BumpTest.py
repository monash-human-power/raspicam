# ---------------------------------------------------------------------
# Last Modified:
#   9-12-2017
# Description:
#   This program reads data from the accelerometer and dumps
#   it to a csv file. It is important to keep this file short as
#   speed of execution is critical.
# ---------------------------------------------------------------------

# ---------------------- Import required libraries --------------------
import IMU
import time
import csv

# ---------------------- Initialise berryIMU --------------------------

IMU.detectIMU()  # Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()  # Initialise the accelerometer, gyroscope and compass

# ---------------------- Start Program --------------------------------

# Open file to print too
filename = "/home/pi/Documents/MHP_raspicam/IMU/Bump Testing/Test Data/Data.csv"
file = open(filename, 'w')
filewrite = csv.writer(file, delimiter=',', lineterminator='\n')

# Record program start time
init_time = time.time()

while True:
    try:
        # Read our accelerometer,gyroscope and magnetometer  values
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()

        # Record time when i2c read ends, calculate difference
        time_elapsed = time.time() - init_time

        # Write information to file
        filewrite.writerow([time_elapsed, ACCx, ACCy, ACCz])

    except KeyboardInterrupt:

        # End program
        print("\n\nEnding Test\n")
        file.close()
        break
