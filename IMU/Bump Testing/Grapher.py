# ---------------------------------------------------------------------
# Last Modified:
#   9-12-2017
# Description:
#   This program reads data from a csv file and graphs it in 1 second
#   intervals.
# ---------------------------------------------------------------------

# ---------------------- Import required libraries --------------------
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ---------------------- Start Program --------------------------------

filename = "/home/pi/Documents/MHP_raspicam/IMU/Data/Data.csv"
fig = plt.figure()


def animate(i):
    file = open(filename)
    graphX = list()
    t = list()
    for line in file:
        fragmented_line = line.split(",")
        time_elapsed = fragmented_line[0]
        ACCx = fragmented_line[1]

        t.append(float(time_elapsed))
        graphX.append(float(ACCx))

        ax1 = fig.add_subplot(1, 1, 1, axisbg="white")
        ax1.clear()
        ax1.plot(t, graphX)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
