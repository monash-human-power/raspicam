# ---------------------------------------------------------------------
# Last Modified:
#   9-12-2017
# Description:
#   This program is the test master. It decides which modules run append
#   and in what order.
# ---------------------------------------------------------------------

import subprocess
from time import sleep

p1 = subprocess.Popen(["python", "data.py"])
print("\nStarting Data Recording...")
sleep(1)

print("Setting Up Graphs...\n")
p2 = subprocess.Popen(["python", "graph.py"])

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()
	print("\n\nExecution Terminated.\n")
	break
