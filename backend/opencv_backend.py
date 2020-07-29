import cv2

from backend import Backend, PublishFunc
from canvas import Canvas

class OpenCVBackend(Backend):
    """ Gets and displays video using the OpenCV (`cv2`) library.

        This is intended for use with laptops with webcams, not on the
        Raspberry Pi. """

    def __init__(self, client:paho.mqtt.client.Client, width: int, height: int, publish_recording_status_func: PublishFunc):
        super().__init__(client, width, height, publish_recording_status_func, publish_errors_func)

        self.webcam = None

        framerate = 60
        # Time between video frames when running on OpenCV, in milliseconds
        self.frametime = int(1000 / framerate)

        self.base_canvas = Canvas(self.width, self.height)
        self.data_canvas = Canvas(self.width, self.height)
        self.message_canvas = Canvas(self.width, self.height)

    def start_video(self) -> None:
        # Uses whatever OpenCV determines to be the "default camera"
        default_camera_index = 0
        self.webcam = cv2.VideoCapture(default_camera_index)

    def _on_base_canvas_updated(self, base_canvas: Canvas) -> None:
        self.base_canvas = base_canvas

    def _on_canvases_updated(self, data_canvas: Canvas, message_canvas: Canvas) -> None:
        self.data_canvas = data_canvas
        self.message_canvas = message_canvas

    def _on_loop(self) -> None:
        """ This function uses the cached overlays, as OpenCV needs us to
            manually add it to each frame. """
        _, frame = self.webcam.read()
        frame = cv2.resize(frame, (self.width, self.height))

        frame = self.base_canvas.copy_to(frame)
        frame = self.data_canvas.copy_to(frame)
        frame = self.message_canvas.copy_to(frame)

        cv2.imshow('frame', frame)
        cv2.waitKey(self.frametime)

    def stop_video(self) -> None:
        self.webcam.release()
        cv2.destroyAllWindows()
