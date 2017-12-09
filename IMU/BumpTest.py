# ---------------------------------------------------------------------
# Last Modified:
#   3-12-2017
# Description:
#   This program reads data from the accelerometer and dumps
#   it to a file. The speed of read and write commands is printed to the
#   terminal interface.
# ---------------------------------------------------------------------

# ---------------------- Import required libraries --------------------
import IMU
import time
import csv
import matplotlib

# ---------------------- Initialise berryIMU --------------------------

IMU.detectIMU()  # Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()  # Initialise the accelerometer, gyroscope and compass

# ---------------------- Start Program --------------------------------

# Open file to print too
filename = "/home/pi/Documents/MHP_raspicam/IMU/Data/Data on #.csv"
filename = filename.replace("#", time.strftime("%d-%m-%Y at %H:%M:%S", time.localtime()))
file = open(filename, 'w')
filewrite = csv.writer(file, delimiter=',', lineterminator='\n')

# Initialise Graph
fig = matplotlib.pyplot.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax1.xlabel("Time (s)")
ax1.ylabel("Acceleration (Raw Values)")
ax1.title("Acceleration over Time")


def animate(i):
    ax1.clear()
    ax1.plot(time_elapsed, ACCx, label="ACCx")
    ax1.plot(time_elapsed, ACCy, label="ACCx")
    ax1.plot(time_elapsed, ACCz, label="ACCx")


# Record program start time
init_time = time.time()

while True:
    try:
        # Read our accelerometer,gyroscope and magnetometer  values
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()

        # Record time when i2c read ends, calculate difference
        end_read = time.time()
        time_elapsed = end_read - init_time

        # Write information to file
        data = "\n%5.20f,%5.2f,%5.2f,%5.2f" % (time_elapsed, ACCx, ACCy, ACCz)
        filewrite.writerow([time_elapsed, ACCx, ACCy, ACCz])

        # Plot information
        ani = matplotlib.animation.FuncAnimation(fig, animate, interval=1000)
        matplotlib.pyplot.show()

    except KeyboardInterrupt:

        # End program
        file.close()
        break

        # Record time when i2c read starts
        #start_read = time.time()

        # Record time when file write ends
        #end_write = time.time()

        # Output loop frequency
        #write_freq = 1 / (end_write - start_read)
        # print "%5.5f" % write_freq
