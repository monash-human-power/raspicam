# ---------------------------------------------------------------------
# Last Modified:
#   3-12-2017
# Description:
#   This program reads data from the accelerometer and dumps
#   it to a file. The speed of read and write commands is printed to the
#   terminal interface.
# ---------------------------------------------------------------------

# ---------------------- Import required libraries --------------------

from i2c import MAG_ADDRESS,ACC_ADDRESS,GYR_ADDRESS,writeACC,writeMAG,writeGRY,readACCx,readACCy,readACCz,readMAGx,readMAGy,readMAGz,readGYRx,readGYRy,readGYRz
from time import localtime, strftime
import time

if MAG_ADDRESS == 0x1E:
    from LSM9DS0 import *
else:
    from LSM9DS1 import *

# ---------------------- Initialise berryIMU --------------------------

# initialise the accelerometer
if MAG_ADDRESS == 0x1E:
    writeACC(CTRL_REG1_XM, 0b10100111)  # z,y,x axis enabled, continuous update,  100Hz data rate
    writeACC(CTRL_REG2_XM, 0b00100000)  # +/- 16G full scale, 773 Hz Anti-Aliasing Bandwidth
else:
    # 119 Hz data rate, +/- 16G full scale, 408 Hz Anti-Aliasing Bandwidth
    writeACC(CTRL_REG6_XL, 0b01101000)
    writeACC(CTRL_REG2_XM, 0b00100000)  # +/- 16G full scale

    # initialise the magnetometer
if MAG_ADDRESS == 0x1E:
    writeMAG(CTRL_REG5_XM, 0b11110000)  # Temp enable, M data rate = 50Hz
    writeMAG(CTRL_REG6_XM, 0b01100000)  # +/-12gauss
    writeMAG(CTRL_REG7_XM, 0b00000000)  # Continuous-conversion mode
else:
    writeMAG(CTRL_REG1_XM, 0b11110000)  # Temp enable, High Resolution, M data rate = 50Hz
    writeMAG(CTRL_REG2_XM, 0b01100000)  # +/-12gauss
    writeMAG(CTRL_REG3_XM, 0b00000000)  # Continuous-conversion mode

# initialise the gyroscope
if MAG_ADDRESS == 0x1E:
    writeGRY(CTRL_REG1_G, 0b00001111)  # ODR = 95 Hz, Cutoff = 12.5 Hz
    writeGRY(CTRL_REG4_G, 0b00110000)  # Continuous update, 2000 dps full scale
else:
    writeGRY(CTRL_REG1_G, 0b01111000)  # ODR = 119 Hz, Cutoff = 14 Hz, 2000 dps

# ---------------------- Start Program --------------------------------

# Open file to print too
filename = "/home/pi/Documents/MHP_raspicam/IMU/Data/Data on #.txt"
filename = filename.replace("#", strftime("%d-%m-%Y at %H:%M:%S", localtime()))
file = open(filename, 'w')

# Record program start time
init_time = time.time()

while True:
    try:
        # Record time when i2c read starts
        start_read = time.time()
        
        # Read our accelerometer,gyroscope and magnetometer  values
        ACCx = readACCx()
        ACCy = readACCy()
        ACCz = readACCz()

        # Record time when i2c read ends, calculate difference
        end_read = time.time()
	time_elapsed = end_read - init_time

	# Write information to file
        data = "\n%5.20f,%5.2f,%5.2f,%5.2f" % (time_elapsed,ACCx,ACCy,ACCz)
        file.write(data)

        # Record time when file write ends
        end_write = time.time()

        # Output loop frequency
        write_freq = 1/(end_write-start_read)
        print "%5.5f" % write_freq
        
    except KeyboardInterrupt:

        # End program
        file.close()
        break
