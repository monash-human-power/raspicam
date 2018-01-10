
import socket
import subprocess

UDP_IP = subprocess.check_output(['hostname','-I'])
#UDP_IP = "192.168.1.101"
UDP_PORT = 5005
start = 1

try:
    print ""
    while True:
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))

        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if start == 1:
	    print "Received Start Command!\n"
	    start = 0
	else:
	    print "Received Stop Command!\n"
	    start = 1
except KeyboardInterrupt:
    print("\n\nProgram Ended.\n")

