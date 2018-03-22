import picamera
import datetime as dt

with picamera.PiCamera() as camera:
    camera.resolution = (800, 480)
    camera.framerate = 24
    camera.start_preview()
    camera.annotate_background = True
    camera.start_recording('test.h264')
    start = dt.datetime.now()
    while (dt.datetime.now() - start).seconds < 30:
	value = dt.datetime.now() - start
	total_seconds = int(value.total_seconds())
	hours, remainder = divmod(total_seconds,60*60)
	minutes, seconds = divmod(remainder,60)

#	camera.annotate_background=picamera.Color('blue')

        camera.annotate_text = '{}:{}:{}'.format(hours,minutes,seconds)
        camera.wait_recording(0.2)
    camera.stop_recording()
