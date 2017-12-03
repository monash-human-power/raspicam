import smbus
bus = smbus.SMBus(1)

# Run sudo i2cdetect -y 1 to check if address is 0x1C or 0x1E, then change below
MAG_ADDRESS = 0x1E
ACC_ADDRESS = MAG_ADDRESS
GYR_ADDRESS = 0x6A

if MAG_ADDRESS == 0x1E:
    from LSM9DS0 import *
else:
    from LSM9DS1 import *

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
