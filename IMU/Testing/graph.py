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

filename = "/home/pi/Documents/MHP_raspicam/IMU/Testing/Test_Data/Data.csv"
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    graph_data = open(filename, 'r').read()
    lines = graph_data.split("\n")
    ts = []
    xs = []
    for line in lines:
	print(len(line))
        if len(line) >= 8:
            t, x, y, z = line.split(",")
            ts.append(t)
            xs.append(x)
    ax1.clear()
    ax1.plot(ts, xs)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
