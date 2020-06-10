import backend

class BackendFactory:
    
    @staticmethod
    def create(backend_name: str, width: int, height: int, publish_recording_status_func) -> backend.Backend:
        backend_name = backend_name.lower()
        if backend_name == "picamera":
            return backend.PiCameraBackend(width, height, publish_recording_status_func)
        elif backend_name == "opencv":
            return backend.OpenCVBackend(width, height, publish_recording_status_func)
        else:
            raise NotImplementedError(f"Unknown backend: {backend_name}")
