import backend

class BackendFactory:
    
    @staticmethod
    def create(width: int, height: int, publish_recording_status_func) -> backend.Backend:
        if backend.ON_PI:
            return backend.PiCameraBackend(width, height, publish_recording_status_func)
        else:
            return backend.OpenCVBackend(width, height, publish_recording_status_func)
