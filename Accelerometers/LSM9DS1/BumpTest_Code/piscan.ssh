#!/bin/bash

PatPiMAC=b8:27:eb:d0:ac:d8
PiZero1MAC=b8:27:eb:b3:52:f
PiZero2MAC=b8:27:eb:8d:cd:e5
PiZero3MAC=b8:27:eb:3b:26:bb

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
        if [ "$MAC" == "$PatPiMAC" ]
        then
            printf "Found Pat Pi\n"
        elif [ "$MAC" == "$PiZero1MAC" ]
        then
            printf "Found Pi Zero 1\n"
        elif [ "$MAC" == "$PiZero2MAC" ]; then
            printf "Found Pi Zero 2\n"
        elif [ "$MAC" == "$PiZero3MAC" ]; then
            printf "Found Pi Zero 3\n"
        fi
    fi
    lsv=$(( $lsv + 1 )) # Increment lower end of ip address count
    ip_scan_range=$(( $ip_scan_range - 1 )) # decrement ip address scan range
done
