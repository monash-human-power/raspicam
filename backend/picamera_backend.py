from enum import Enum
from typing import Dict

from backend import Backend
from overlay import Canvas

try:
    from picamera import PiCamera
    ON_PI = True
except (ImportError, RuntimeError):
    ON_PI = False

PI_WINDOW_TOP_LEFT = (0, -20)

class OverlayLayer(Enum):
    video_feed = 2
    base = 3
    data = 4
    message = 5

class PiCameraBackend(Backend):

    def __init__(self):
        super().__init__()
        self.pi_camera = PiCamera(resolution=(self.width, self.height))

        self.prev_overlays: Dict[OverlayLayer, self.pi_camera.PiOverlayRenderer] = {}

    def start_video(self):
        # Start displaying video feed. Non blocking, but runs forever in seperate thread.
        self.pi_camera.start_preview(fullscreen=False, window=(*PI_WINDOW_TOP_LEFT, self.width, self.height))

    def update_picamera_overlay(self, canvas: Canvas, layer: OverlayLayer):
        """ Adds the overlay to a PiCamera preview, and if the overlay was already added,
            removes the old instance. """
        overlay = self.pi_camera.add_overlay(canvas.img, format="rgba", size=(self.width, self.height))
        overlay.layer = layer.value
        overlay.fullscreen = False
        overlay.window = (*PI_WINDOW_TOP_LEFT, self.width, self.height)

        # Rather than creating and swapping out overlays, the proper way to do this would be with overlay.update()
        # Unfortunately, due to a bug in PiCamera 1.13, this will spam us with errors (which don't matter, but still)
        # https://github.com/waveform80/picamera/issues/320
        # https://www.raspberrypi.org/forums/viewtopic.php?t=190120
        if layer in self.prev_overlays:
            self.pi_camera.remove_overlay(self.prev_overlays[layer])
        self.prev_overlays[layer] = overlay

    def on_base_overlay_update(self, base_canvas: Canvas):
        self.update_picamera_overlay(base_canvas, OverlayLayer.base)

    def on_overlays_updated(self, data_canvas: Canvas, message_canvas: Canvas):
        """ Picamera will retain the overlay images until updated, so we only need
            to do this once per overlay update. """
        self.update_picamera_overlay(data_canvas, OverlayLayer.data)
        self.update_picamera_overlay(message_canvas, OverlayLayer.message)

    def stop_video(self):
        self.pi_camera.stop_preview()
        self.stop_recording()
        self.pi_camera.close()