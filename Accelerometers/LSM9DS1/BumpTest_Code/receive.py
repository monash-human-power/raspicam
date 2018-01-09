import socket

UDP_IP = "PatPi.local"  # CHANGE TO DESTINATION IP ADDRESS
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print "Received command!:", data
    break


# subprocess.call(
#    '/home/pi/Documents/MHP_raspicam/Accelerometers/LSM9DS1/BumpTest_Code/Shell_Scripts/sendcsv.sh')
