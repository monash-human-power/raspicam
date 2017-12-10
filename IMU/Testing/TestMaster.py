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
        # Get process id
        pid1 = p1.pid
        pid2 = p2.pid

        # Try to terminate gracefully
        p1.terminate()
        p2.terminate()

        # Check if you need to force kill
        try:
            os.kill(pid1, 0)
            os.kill(pid2, 0)
            p1.kill()
            p2.kill()
            print ("\nForced kill\n")
        except OSError, e:
            print("\nTerminated Gracefully\n")
