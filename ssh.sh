#!/bin/bash

# Obtain local net id. For me this is 10.1.1.0
NET=$(ip route get 8.8.8.8 | awk '{print $NF; exit}')

# Use local net ID to find raspberry pi on local network using MAC Address. Loop here until pi is online.
while [ -z "$temp" ];
do
temp=$(sudo nmap -sP $NET/24 | awk '/^Nmap/{ip=$NF}/B8:27:EB/{print ip}')
done

# Remove parathensis from temp output
new_temp=$(echo $temp|sed 's/(//g')  
PI_IP=$(echo $new_temp|sed 's/)//g')

# Define pi username
USERNAME=pi

# Begin ssh session
ssh ${USERNAME}@${PI_IP}
