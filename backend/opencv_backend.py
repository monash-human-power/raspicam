import cv2

from backend import Backend
from overlay import Canvas

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