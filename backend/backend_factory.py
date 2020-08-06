import backend


class BackendFactory:
    @staticmethod
    def create(
        backend_name: str,
        width: int,
        height: int,
        publish_recording_status_func,
        exception_handler,
    ) -> backend.Backend:
        backend_name = backend_name.lower()
        if backend_name == "picamera":
            return backend.PiCameraBackend(
                width, height, publish_recording_status_func, exception_handler
            )
        elif backend_name == "opencv":
            return backend.OpenCVBackend(
                width, height, publish_recording_status_func, exception_handler
            )
        elif backend_name == "opencv_static_image":
            return backend.OpenCVStaticImageBackend(
                width, height, publish_recording_status_func, exception_handler
            )
        else:
            raise NotImplementedError(f"Unknown backend: {backend_name}")
