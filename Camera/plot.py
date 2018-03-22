# ---------------------------------------------------------------------
# Last Modified:
#   30-12-2017
# Description:
#   This program reads data from a csv file and graphs it in 1 second
#   intervals.
# ---------------------------------------------------------------------

# ---------------------- Import required libraries --------------------
import matplotlib.pyplot as plt
import numpy

# ---------------------- Start Program --------------------------------

plt.close('all')
win = 200  # window length

#name = raw_input("Enter the filename you wish to graph (with file extension): ")
#filename = "/home/pi/Documents/Received_Data/"+name
filename = "/home/pi/Documents/MHP_raspicam/Velocity/speed.csv"
graph_data = open(filename, 'r').read()
lines = graph_data.split("\n")

# Setup Plots
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

ts = []
binary = []

# Extract Data
for line in lines:
    if len(line) > 0:
        parts = line.split(",")
        if len(parts) == 2:
            # Rescale Data into g's
            parts[1] = int(parts[1]) * Sensitivity
            parts[2] = int(parts[2])

            ts.append(parts[0])
            xs.append(parts[1])

plt.plot(ts, xs, color='r', label='x')
plt.legend()

ts = map(float, ts)
fs = len(ts) / ts[-1]
plt.show()
