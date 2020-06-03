from abc import ABC, abstractmethod

from overlay import Canvas
from backend import PiCameraBackend, ON_PI, OpenCVBackend

def get_backend(width, height):
    if ON_PI:
        return PiCameraBackend
    else:
        return OpenCVBackend

class Backend(ABC):

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.recording = False

    def start_video(self):
        pass

    def on_base_overlay_update(self, base_overlay: Canvas):
        pass

    def on_overlays_updated(self, data_canvas: Canvas, message_canvas: Canvas):
        pass

    def on_loop(self):
        """ Creates the next frame using the webcam and canvases, and displays
            result. """
        pass

    def stop_video(self):
        pass

    def start_recording(self):
        print(f"WARNING: Recording is not supported with {type(self).__name__}")

    def stop_recording(self):
        print(f"WARNING: Recording is not supported with {type(self).__name__}")

    def send_recording_status(self):
        pass

    def send_recording_error(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_video()