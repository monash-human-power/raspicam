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
        if len(line) > 1:
            components = line.split(",")
            ts.append(components[0])
            xs.append(components[1])
    ax1.clear()
    ax1.plot(ts, xs)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
