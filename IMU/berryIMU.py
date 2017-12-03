# ---------------------------------------------------------------------
# Last Modified:
#   3-12-2017
# Description:
#   This program 
#   it to a file. The speed of read and write commands is printed to the
#   terminal interface.
# ---------------------------------------------------------------------

# ---------------------- Import required libraries --------------------

from i2c import MAG_ADDRESS,ACC_ADDRESS,GYR_ADDRESS,writeACC,writeMAG,writeGRY,readACCx,readACCy,readACCz,readMAGx,readMAGy,readMAGz,readGYRx,readGYRy,readGYRz
from time import localtime, strftime
import math
import datetime

if MAG_ADDRESS == 0x1E:
    from LSM9DS0 import *
else:
    from LSM9DS1 import *

# ---------------------- Initialise berryIMU --------------------------

# initialise the accelerometer
if MAG_ADDRESS == 0x1E:
    writeACC(CTRL_REG1_XM, 0b01100111)  # z,y,x axis enabled, continuous update,  100Hz data rate
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

# Initialize Variables
RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
# [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
G_GAIN = 0.070
LP = 0.041      # Loop period = 41ms.   This needs to match the time it takes each loop to run
AA = 0.80      # Complementary filter constant
gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0

# Open file to print too
filename = "/home/pi/Documents/MHP_raspicam/IMU/Data/Data on #.txt"
filename = filename.replace("#", strftime("%d-%m-%Y at %H:%M:%S", localtime()))
file = open(filename, 'w')

while True:
    try:
        a = datetime.datetime.now()

        # Read our accelerometer,gyroscope and magnetometer  values
        ACCx = readACCx()
        ACCy = readACCy()
        ACCz = readACCz()
        GYRx = readGYRx()
        GYRy = readGYRx()
        GYRz = readGYRx()
        MAGx = readMAGx()
        MAGy = readMAGy()
        MAGz = readMAGz()

        # Convert Accelerometer values to degrees
        AccXangle = (math.atan2(ACCy, ACCz) + M_PI) * RAD_TO_DEG
        AccYangle = (math.atan2(ACCz, ACCx) + M_PI) * RAD_TO_DEG

        # Convert Gyro raw to degrees per second
        rate_gyr_x = GYRx * G_GAIN
        rate_gyr_y = GYRy * G_GAIN
        rate_gyr_z = GYRz * G_GAIN

        # Calculate the angles from the gyro. LP = loop period
        gyroXangle += rate_gyr_x * LP
        gyroYangle += rate_gyr_y * LP
        gyroZangle += rate_gyr_z * LP

        # Change the rotation value of the accelerometer to -/+ 180 and move the Y axis '0' point to up.
        # Two different pieces of code are used depending on how your IMU is mounted.
        # If IMU is upside down
        #
        # if AccXangle >180:
        #        AccXangle -= 360.0
        # AccYangle-=90
        # if (AccYangle >180):
        #        AccYangle -= 360.0

        # If IMU is up the correct way, use these lines
        AccXangle -= 180.0
        if AccYangle > 90:
            AccYangle -= 270.0
        else:
            AccYangle += 90.0

        # Complementary filter used to combine the accelerometer and gyro values.
        CFangleX = AA * (CFangleX + rate_gyr_x * LP) + (1 - AA) * AccXangle
        CFangleY = AA * (CFangleY + rate_gyr_y * LP) + (1 - AA) * AccYangle

        # Calculate heading
        heading = 180 * math.atan2(MAGy, MAGx) / M_PI

        if heading < 0:
            heading += 360

        # Normalize accelerometer raw values.
        accXnorm = ACCx / math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
        accYnorm = ACCy / math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

        # Calculate pitch and roll
        pitch = math.asin(accXnorm)
        roll = -math.asin(accYnorm / math.cos(pitch))

        # Calculate the new tilt compensated values
        magXcomp = MAGx * math.cos(pitch) + MAGz * math.sin(pitch)
        magYcomp = MAGx * math.sin(roll) * math.sin(pitch) + MAGy * \
            math.cos(roll) - MAGz * math.sin(roll) * math.cos(pitch)

        # Calculate tiles compensated heading
        tiltCompensatedHeading = 180 * math.atan2(magYcomp, magXcomp) / M_PI

        if tiltCompensatedHeading < 0:
            tiltCompensatedHeading += 360

        print ("\033[1;34;40mACCX Angle %5.2f ACCY Angle %5.2f\033[1;31;40m\tGRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f \033[1;35;40m    \tCFangleX Angle %5.2f \033[1;36;40m  CFangleY Angle %5.2f \33[1;32;40m  HEADING  %5.2f \33[1;37;40m tiltCompensatedHeading %5.2f\033[0m  " % (
            AccXangle, AccYangle, gyroXangle, gyroYangle, gyroZangle, CFangleX, CFangleY, heading, tiltCompensatedHeading))

        data = "\nACCX_Angle %5.2f\tACCY_Angle %5.2f\t\tGRYX_Angle %5.2f\tGYRY_Angle %5.2f\tGYRZ_Angle %5.2f\t\tCFangleX_Angle %5.2f\tCFangleY_Angle %5.2f\t\tHEADING  %5.2f\ttiltCompensatedHeading %5.2f" % (
            AccXangle, AccYangle, gyroXangle, gyroYangle, gyroZangle, CFangleX, CFangleY, heading, tiltCompensatedHeading)
        file.write(data)

        # time.sleep(1)
        # print(roll)
        # print "Loop Time |",  c.microseconds/1000,"|",

    except KeyboardInterrupt:

        file.close()
        break
