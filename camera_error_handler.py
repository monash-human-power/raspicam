from json import dumps
from traceback import format_exc

from topics import Camera


class CameraErrorHandler:
    """
    Exception handler for the Raspicam

    Use alongside the 'with' magic Python word.
    eg. with CameraException(client, camera, backend_name, bg_path, configs)
    """

    def __init__(
        self, client, camera: str, backend: str, bg_path: str, configs: dict
    ):
        self.client = client
        self.camera = camera
        self.backend = backend
        self.bg_path = bg_path
        self.configs = configs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Handle any exception thrown, if an error occured. """
        if exc_type is Exception:
            message = {
                "camera": self.camera,
                "backend": self.backend,
                "bg_path": self.bg_path,
                "configs": self.configs,
                "traceback": format_exc(),
                "message": str(exc_value),
            }

            status_topic = str(Camera.errors)
            self.client.publish(status_topic, dumps(message))
