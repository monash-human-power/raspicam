# MODEL B SIDE

import subprocess
import socket

PatPiMAC='b8:27:eb:d0:ac:d8'
#PatMacbookMAC='6c:40:08:99:ce:b0'
PiZero1MAC='b8:27:eb:b3:52:f'
PiZero2MAC='b8:27:eb:8d:cd:e5'
PiZero3MAC='b8:27:eb:3b:26:bb'

MAC_List = [PatPiMAC,PiZero1MAC,PiZero2MAC,PiZero3MAC]

index = 0
Online_List=[0] * len(MAC_List)
for MAC in MAC_List:
    IP=subprocess.check_output(['./piscan.sh',MAC])
    if IP != 0:
        Online_List[index]=IP
    index = index + 1

for IP in Online_List:
    if IP == '0':
        continue
    
    UDP_IP = IP
    UDP_PORT = 5005
    
    MESSAGE = "Hello!"
    
    print "UDP target IP:", UDP_IP
    print "UDP target port:", UDP_PORT
    print "message:", MESSAGE
    
    sock = socket.socket(socket.AF_INET,  # Internet
                 socket.SOCK_DGRAM)  # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))