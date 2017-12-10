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

plt.close('all')

filename = "/home/pi/Documents/MHP_raspicam/IMU/Testing/Test_Data/Data.csv"
fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey = True)
fig.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

def animate(i):
    graph_data = open(filename, 'r').read()
    lines = graph_data.split("\n")
    ts = []
    xs = []
    ys = []
    zs = []
    for line in lines:
        if len(line) > 0:
            parts = line.split(",")
            if len(parts) == 4:
                ts.append(parts[0])
                xs.append(parts[1])
		ys.append(parts[2])
		zs.append(parts[3])
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax1.plot(ts[-200:-1], xs[-200:-1],color='r',label="ACCx")
    ax1.legend()
    ax2.plot(ts[-200:-1], ys[-200:-1],color='b',label="ACCy")
    ax2.legend()
    ax3.plot(ts[-200:-1], zs[-200:-1],color='k',label="ACCz")
    ax3.legend()
    ax1.set_title("Raw Acceleration Values Over Time")
    ax3.set_xlabel("Time (s)")
    ax2.set_ylabel("Acceleration (g)")

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
