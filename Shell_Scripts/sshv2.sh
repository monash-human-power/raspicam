#!/bin/bash

# This script automates ssh connection using the network ping utility. It is
# appropriate only when a pi is attempting to connect to Telstra 4G USB Modem.
# It should not be used in any other scenario.

# Known and recognised Target Pi's.
USERNAME=pi # all pi's have same username
PiZero1MAC=b8:27:eb:b3:52:f
PiZero2MAC=b8:27:eb:8d:cd:e5

# Select Target Pi (either manually or through user input)
#TargetPi = 1 # Assign manually in script
printf "\nKNOWN PI'S";
printf "\n\tName:\t\tID:\tMAC Address:"
printf "\n\tPi Zero 1\t1\t$PiZero1MAC"
printf "\n\tPi Zero 2\t2\t$PiZero2MAC\n"
printf "\nSelect target Pi ID = "; read TargetPi # Read from user input

# Choose MAC Address to Search for
if [ $TargetPi == 1 ]
then
    SearchMAC=$PiZero1MAC # CHANGE THIS TO THE PI YOU WANT TO SSH INTO
elif [ $TargetPi == 2 ]
then
    SearchMAC=$PiZero2MAC
else
    printf "\nInvalid Input. Program Terminated.\n\n"
    exit 0
fi

# Scan Criteria (Based on Router dhcp allocation range)
start_ip=192.168.1.100
ip_scan_range=10

# Prepare for loop
ssh=0 # do not initiate ssh connection
baseaddr="$(echo $start_ip | cut -d. -f1-3)"
lsv="$(echo $start_ip | cut -d. -f4)"

# Scan for Pi
while [ $ip_scan_range -gt 0 ] # Terminate loop when scan range == 0
do
    # Increment scan ip address
    addr="$(echo $baseaddr.$lsv)"

    # Ping that address to check for host
    fping=$(fping -c 1 -t 500 $addr 2>/dev/null | sort)

    # If ping returns non-empty information, host is online
    if [ ! -z "$fping" ]
    then
        # Notify host has been found
        printf "\nFound Active Host\n"

        # Find the MAC address associated with that IP Address
        MAC=$(arp -n $addr | awk '{print $4}')
        printf "MAC Address = $MAC\n" # Print MAC Address

        # Check to see if MAC Address is one of list of known Pi's.
        if [ "$MAC" == "$PiZero1MAC" ]
        then
            printf "Found Pi Zero 1\n"
        elif [ "$MAC" == "$PiZero2MAC" ]; then
            printf "Found Pi Zero 2\n"
        fi

        # Check to see if MAC Address is that of Target Pi
        if [ "$MAC" == "$SearchMAC" ]
        then
            ssh=1 # initiate ssh connection once exited loop
            PI_IP=$addr # assign ssh IP Address
            printf "Target Pi Found @ $PI_IP\n" # Notify found target pi
            break #break from loop
        fi
    fi
    lsv=$(( $lsv + 1 )) # Increment lower end of ip address count
    ip_scan_range=$(( $ip_scan_range - 1 )) # decrement ip address scan range
done

# If statement will be activated if target pi is found
if [ $ssh == 1 ]
then
    printf "\nStarting ssh connection...\n\n"
    ssh ${USERNAME}@${PI_IP} # SSH session begins
else
    printf "\nFailed to find target Pi. Check to see if Pi is online.\n"
fi

printf "\n" # add new line for neatness
exit 0 # end of program

## Code when looking for just any Pi
#TempMAC=$(echo $MAC |rev|cut -d":" -f4-|rev)
#echo "MAC Address begins with $TempMAC"
