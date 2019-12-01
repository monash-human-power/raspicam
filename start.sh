#!/bin/sh
docker run -it --rm \
    -v $(pwd):/cam \
    -e MQTT_BROKER_IP=${MQTT_BROKER_IP:-host.docker.internal} \
    -e DISPLAY=host.docker.internal:0.0 \
    --device ${CAM_PATH:-/dev/video0}:/dev/video0 \
    mhp/raspicam "$@"
