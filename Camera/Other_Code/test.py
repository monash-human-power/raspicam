import picamera
import datetime as dt

with picamera.PiCamera() as camera:

    # Configure Camera
    camera.resolution = (800, 480)
    camera.framerate = 24
    camera.annotate_background = True
    camera.start_preview()

    # Start Recording with given filename
    camera.start_recording('test.h264')

    # Start time
    start = dt.datetime.now()

    # Begin Loop
    while (dt.datetime.now() - start).seconds < 30:
        # Calculate time delta
        value = dt.datetime.now() - start

        # Convert to hours, minutes, seconds
        total_seconds = int(value.total_seconds())
        hours, remainder = divmod(total_seconds, 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        # Overlay on to Camera Feed
        camera.annotate_text = '{}:{}:{}'.format(hours, minutes, seconds)

        # Wait before repeating loop
        camera.wait_recording(0.2)

    # Stop recording after 30 seconds
    camera.stop_recording()
