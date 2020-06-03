from abc import ABC, abstractmethod

class Renderer(ABC):

    def __init__(self):
        self.recording = False

    def start_video(self):
        pass

    def update_overlays(self):
        pass

    def show_frame(self):
        pass

    def stop_video(self):
        pass

    def start_recording(self):
        print(f"WARNING: Recording is not with {type(self).__name__}")

    def stop_recording(self):
        print(f"WARNING: Recording is not with {type(self).__name__}")

    def send_recording_status(self):
        pass

    def send_recording_error(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_video()