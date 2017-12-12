# ---------------------------------------------------------------------
# Last Modified:
#   9-12-2017
# Description:
#   This program is the test master. It decides which modules run append
#   and in what order.
# ---------------------------------------------------------------------

import subprocess
from time import sleep

p1 = subprocess.Popen(["python", "datav1.py"])
print("\nStarting Data Recording v1...")
sleep(1)

#p2 = subprocess.Popen(["python", "datav2.py"])
#print("\nStarting Data Recording v2...")
#sleep(1)

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        p1.terminate()
        #p2.terminate()
	print("\n\nExecution Terminated.\n")
	break
