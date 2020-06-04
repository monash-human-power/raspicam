from backend import Backend, PiCameraBackend, OpenCVBackend, ON_PI

class BackendFactory:
    
    @staticmethod
    def create(width: int, height: int, publish_recording_status_func) -> Backend:
        if ON_PI:
            return PiCameraBackend(width, height, publish_recording_status_func)
        else:
            return OpenCVBackend(width, height, publish_recording_status_func)