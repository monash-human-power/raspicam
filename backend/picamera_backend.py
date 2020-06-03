from enum import Enum

from backend import Backend
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