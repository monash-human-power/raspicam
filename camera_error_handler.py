"""
Exception handler for the Raspicam

Used alongside the 'with' magic Python word.
eg. with CameraException(self.client, self.backend_name)
"""
from json import dumps
from traceback import format_exc

from config import read_configs
from topics import Camera

class CameraException:

    def __init__(self, client, backend:str):
        self.configs = read_configs()
        self.client = client
        self.camera = self.configs["device"]
        self.backend = backend

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type is Exception:
            message = {
                "camera": self.camera,
                "backend": self.backend,
                "configs": self.configs,
                "traceback": format_exc(),
                "message": str(value)
            }

            status_topic = f"{str(Camera.errors)}"
            publish_result = self.client.publish(status_topic, dumps(message))
