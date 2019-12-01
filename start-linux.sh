#!/bin/sh
docker run -it --rm \
    -v $(pwd):/cam \
    -e MQTT_BROKER_IP=${MQTT_BROKER_IP:-172.17.0.1} \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --device ${CAM_PATH:-/dev/video0}:/dev/video0 \
    mhp/raspicam "$@"
