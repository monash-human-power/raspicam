# ---------------------------------------------------------------------
#    This program  reads the angles from the acceleromter, gyrscope
#    and mangnetometeron a BerryIMU connected to a Raspberry Pi.
#
#       		http://ozzmaker.com/
#
#    Copyright (C) 2015  Mark Williams
# ---------------------------------------------------------------------
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Library General Public
#    License as published by the Free Software Foundation; either
#    version 2 of the License, or (at your option) any later version.
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    Library General Public License for more details.
#    You should have received a copy of the GNU Library General Public
#    License along with this library; if not, write to the Free
#    Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
#    MA 02111-1307, USA
# ---------------------------------------------------------------------

# Run sudo i2cdetect -y 1 to check if address is 0x1C or 0x1E, then change below
MAG_ADDRESS = 0x1C
ACC_ADDRESS = MAG_ADDRESS
GYR_ADDRESS = 0x6A

if MAG_ADDRESS == 0x1E:
    from LSM9DS0 import *
else:
    from LSM9DS1 import *

import i2c.py
from time import localtime, strftime
import math
import datetime
import smbus
bus = smbus.SMBus(1)

filename = "/home/pi/Documents/MHP_raspicam/Data/Data on #.txt"
filename = filename.replace("#", strftime("%d-%m-%Y at %H:%M:%S", localtime()))
file = open(filename, 'w')

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
# [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
G_GAIN = 0.070
LP = 0.041      # Loop period = 41ms.   This needs to match the time it takes each loop to run
AA = 0.80      # Complementary filter constant

# COMMANDS TO WRITE ON I2C BUS


def writeACC(register, value):
    bus.write_byte_data(ACC_ADDRESS, register, value)
    return -1


def writeMAG(register, value):
    bus.write_byte_data(MAG_ADDRESS, register, value)
    return -1


def writeGRY(register, value):
    bus.write_byte_data(GYR_ADDRESS, register, value)
    return -1

# COMMANDS TO READ FROM I2C BUS


def readACCx():
    if MAG_ADDRESS == 0x1E:
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_A)
    else:
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_XL)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_XL)
    acc_combined = (acc_l | acc_h << 8)
    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def readACCy():
    if MAG_ADDRESS == 0x1E:
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_A)
    else:
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_XL)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_XL)
    acc_combined = (acc_l | acc_h << 8)
    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def readACCz():
    if MAG_ADDRESS == 0x1E:
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_A)
    else:
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_XL)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_XL)
    acc_combined = (acc_l | acc_h << 8)
    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def readMAGx():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_X_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_X_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def readMAGy():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Y_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Y_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def readMAGz():
    mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Z_L_M)
    mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Z_H_M)
    mag_combined = (mag_l | mag_h << 8)

    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def readGYRx():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_X_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_X_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def readGYRy():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Y_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Y_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def readGYRz():
    gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
    gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)

    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


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

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0

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

        print "\n%5.2f" % a
        #data = "\n%5.2f,%5.2f,%5.2f,%5.2f,%5.2f,%5.2f,%5.2f,%5.2f,%5.2f" % (ACCx,ACCy,ACCz,GYRx,GYRy,GYRz,MAGx,MAGy,MAGz)
        # file.write(data)

    except KeyboardInterrupt:

        file.close()
        break
