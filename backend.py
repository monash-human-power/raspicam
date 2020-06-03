from abc import ABC, abstractmethod
from enum import Enum

import cv2

from overlay import Canvas

try:
    from picamera import PiCamera
    ON_PI = True
except (ImportError, RuntimeError):
    ON_PI = False

PI_WINDOW_TOP_LEFT = (0, -20)

class PiCameraOverlayLayer(Enum):
    video_feed = 2
    base = 3
    data = 4
    message = 5

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

class PiCameraBackend(Backend):

    def __init__(self):
        super().__init__()
        self.pi_camera = PiCamera(resolution=(self.width, self.height))

    def start_video(self):
        # Start displaying video feed. Non blocking, but runs forever in seperate thread.
        self.pi_camera.start_preview(fullscreen=False, window=(*PI_WINDOW_TOP_LEFT, self.width, self.height))

    def on_base_overlay_update(self, base_canvas: Canvas):
        base_canvas.update_pi_overlay(self.pi_camera, PiCameraOverlayLayer.base)

    def on_overlays_updated(self, data_canvas: Canvas, message_canvas: Canvas):
        """ Picamera will retain the overlay images until updated, so we only need
            to do this once per overlay update. """
        data_canvas.update_pi_overlay(self.pi_camera, PiCameraOverlayLayer.data)
        message_canvas.update_pi_overlay(self.pi_camera, PiCameraOverlayLayer.message)

    def stop_video(self):
        self.pi_camera.stop_preview()
        self.stop_recording()
        self.pi_camera.close()

class OpenCVBackend(Backend):

    def __init__(self):
        super().__init__()
        self.webcam = cv2.VideoCapture(0)

        # Time between video frames when running on OpenCV, in milliseconds
        self.frametime = 17

        self.base_canvas = Canvas(self.width, self.height)
        self.data_canvas = Canvas(self.width, self.height)
        self.message_canvas = Canvas(self.width, self.height)

    def on_base_overlay_update(self, base_canvas: Canvas):
        self.base_canvas = base_canvas

    def on_overlays_updated(self, data_canvas: Canvas, message_canvas: Canvas):
        self.data_canvas = data_canvas
        self.message_canvas = message_canvas

    def on_loop(self):
        """ This function uses the cached overlay, as OpenCV needs us to
            manually add it to each frame. """
        _, frame = self.webcam.read()
        frame = cv2.resize(frame, (self.width, self.height))

        frame = self.base_canvas.copy_to(frame)
        frame = self.data_canvas.copy_to(frame)
        frame = self.message_canvas.copy_to(frame)

        cv2.imshow('frame', frame)
        cv2.waitKey(self.frametime)