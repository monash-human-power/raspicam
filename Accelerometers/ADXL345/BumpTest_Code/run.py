# ---------------------------------------------------------------------
# Last Modified:
#   30-12-2017
# Description:
#   This program is the test master. It decides which modules run append
#   and in what order.
# ---------------------------------------------------------------------

import subprocess
from subprocess import call
from time import sleep

send = 0

p1 = call(['sudo', '/home/pi/Documents/MHP_raspicam/Accelerometers/ADXL345/BumpTest_Code/data.c'])
print("\nStarting Data Recording..")
sleep(1)

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        p1.terminate()
        print("\n\nExecution Terminated.\n")
        break

if send == 1:
    p3 = subprocess.call(
        '/home/pi/Documents/MHP_raspicam/Accelerometers/LSM9DS1/BumpTest_Code/Shell_Scripts/sendcsv.sh')
    sleep(1)
