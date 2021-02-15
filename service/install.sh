#!/bin/bash

SERVICE_DIR=$HOME/.config/systemd/user
RASPICAM_DIR=$(dirname $(cd $(dirname "${BASH_SOURCE[0]}") && pwd))

# Create folder for service if it doesn't yet exist
mkdir -p $SERVICE_DIR
# Copy service files to service directory
cp $RASPICAM_DIR/service/raspicam-orchestrator.service $SERVICE_DIR
cp $RASPICAM_DIR/service/raspicam-switch.service $SERVICE_DIR

# Append working directory to service file
echo WorkingDirectory=$RASPICAM_DIR >> $SERVICE_DIR/raspicam-orchestrator.service
echo WorkingDirectory=$RASPICAM_DIR >> $SERVICE_DIR/raspicam-switch.service
