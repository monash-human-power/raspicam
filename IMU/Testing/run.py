# ---------------------------------------------------------------------
# Last Modified:
#   9-12-2017
# Description:
#   This program is the test master. It decides which modules run append
#   and in what order.
# ---------------------------------------------------------------------

import subprocess
from time import sleep

p1 = subprocess.Popen(["python", "Data.py"])
sleep(0.1)
p2 = subprocess.Popen(["python", "Grapher.py"])
sleep(0.1)

while True:
    try:
        print("Executing...")
        sleep(1)
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()
	print("\nExecution Terminated\n")
	break
