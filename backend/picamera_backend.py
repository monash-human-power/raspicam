from enum import Enum
from time import time
from typing import Dict

from backend import Backend, PublishFunc
from canvas import Canvas
from config import read_configs

# This check needs to be done here, as it's only place we use picamera.
try:
    from picamera import PiCamera

    ON_PI = True
except (ImportError, RuntimeError):
    ON_PI = False

# Top of window is outside the screen to hide title bar
PI_WINDOW_TOP_LEFT = (0, -20)


class PiCameraOverlayLayer(Enum):
    """ The `picamera` layers which each overlay canvas should be placed on.

        Higher layer numbers are placed in front of lower ones. """

    video_feed = 2
    base = 3
    data = 4
    message = 5


class PiCameraBackend(Backend):
    """ Gets video and displays using the `picamera` library.

        This backend will only work when the `picamera` library is available,
        i.e. when running on a Raspberry Pi. """

    def __init__(
        self,
        width: int,
        height: int,
        publish_recording_status_func: PublishFunc,
        publish_video_status_func: PublishFunc,
        exception_handler: PublishFunc,
    ):
        super().__init__(
            width,
            height,
            publish_recording_status_func,
            publish_video_status_func,
            exception_handler,
        )

        if not ON_PI:
            raise RuntimeError(
                "`picamera` library unavailable - please run on Pi or install \
                    library"
            )

        self.pi_camera = PiCamera(resolution=(self.width, self.height))

        configs = read_configs()
        self.pi_camera.brightness = configs["brightness"]
        self.pi_camera.contrast = configs["contrast"]

        self.prev_overlays: Dict[
            PiCameraOverlayLayer, self.pi_camera.PiOverlayRenderer
        ] = {}

    def _is_video_on(self):
        return self.pi_camera.previewing

    def start_video(self) -> None:
        """Start displaying video feed.

        Non blocking, but runs forever in separate thread.
        """
        self.pi_camera.start_preview(
            fullscreen=False,
            window=(*PI_WINDOW_TOP_LEFT, self.width, self.height),
        )

    def update_picamera_overlay(
        self, canvas: Canvas, layer: PiCameraOverlayLayer
    ) -> None:
        """Adds the overlay to a PiCamera preview.

        If the overlay was already added, removes the old instance.
        """
        overlay = self.pi_camera.add_overlay(
            canvas.img, format="rgba", size=(self.width, self.height)
        )
        overlay.layer = layer.value
        overlay.fullscreen = False
        overlay.window = (*PI_WINDOW_TOP_LEFT, self.width, self.height)

        """
        Rather than creating and swapping out overlays, the proper way to do
        this would be with overlay.update(). Unfortunately, due to a bug in
        PiCamera 1.13, this will spam us with errors.
        (which don't matter, but still)
        https://github.com/waveform80/picamera/issues/320
        https://www.raspberrypi.org/forums/viewtopic.php?t=190120
        """
        if layer in self.prev_overlays:
            self.pi_camera.remove_overlay(self.prev_overlays[layer])
        self.prev_overlays[layer] = overlay

    def _on_base_canvas_updated(self, base_canvas: Canvas) -> None:
        self.update_picamera_overlay(base_canvas, PiCameraOverlayLayer.base)

    def _on_canvases_updated(
        self, data_canvas: Canvas, message_canvas: Canvas
    ) -> None:
        """ Picamera will retain the overlay images until updated, so we only need
            to do this once per overlay update. """
        self.update_picamera_overlay(data_canvas, PiCameraOverlayLayer.data)
        self.update_picamera_overlay(
            message_canvas, PiCameraOverlayLayer.message
        )

    def _on_loop(self) -> None:
        # Nothing to do
        pass

    def stop_video(self) -> None:
        self.pi_camera.stop_preview()
        self.stop_recording()
        self.pi_camera.close()

    def _start_recording(self) -> None:
        self.pi_camera.start_recording(self.recording_output_file)
        self.recording = True
        self.recording_start_time = time()
        self.pi_camera.wait_recording(0.1)

    def _stop_recording(self) -> None:
        if self.pi_camera.recording:
            self.pi_camera.stop_recording()

    def check_recording_errors(self) -> None:
        self.pi_camera.wait_recording()
