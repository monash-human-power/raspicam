"""
Exception handler for the Raspicam

Used alongside the 'with' magic Python word.
eg. with CameraException(self.client, self.backend_name)
"""
from json import dumps
from traceback import format_exc

from config import read_configs
from topics import Camera

class CameraErrorHandler:

    def __init__(self, client, backend:str):
        self.configs = read_configs()
        self.client = client
        self.camera = self.configs["device"]
        self.backend = backend

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is Exception:
            message = {
                "camera": self.camera,
                "backend": self.backend,
                "configs": self.configs,
                "traceback": format_exc(),
                "message": str(exc_value)
            }

            status_topic = str(Camera.errors)
            self.client.publish(status_topic, dumps(message))
