from json import dumps

from config import read_configs
from topics import Camera

class CameraErrorHandler:
    def __init__(self, client, camera, backend, bg_path):
        self.client = client
        self.camera = camera
        self.backend = backend
        self.bg_path = bg_path

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        message = {
            "camera": self.camera,
            "backend": self.backend,
            "bg_path": self.bg_path,
            "configs": read_configs(),
            "traceback": traceback,
            "message": value
        }

        status_topic = f"{str(Camera.errors)}"
        publish_result = self.client.publish(status_topic, dumps(message))

if __name__ == '__main__':
    with CameraErrorHandler():
        raise Exception("Test error")