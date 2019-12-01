#!/bin/bash

# Make sure the cam user is in group that can access webcam
GROUP_ID=$(ls -ng /dev/video0 | awk '{print $3}')
GROUP_EXISTS=$(getent group $GROUP_ID)
if [[ -z $GROUP_EXISTS ]]; then
    groupadd -g $GROUP_ID $GROUP_ID
fi
GROUP_NAME=$(getent group $GROUP_ID | cut -d: -f1)
usermod -aG $GROUP_NAME cam

# X11 fails to start as root user
su -s /bin/bash -c "/usr/local/bin/python $@" cam
