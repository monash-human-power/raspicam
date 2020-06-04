from abc import ABC
from json import dumps
from os import mkdir, path
from shutil import disk_usage
from time import time
from traceback import format_exc

from overlay import Canvas

class Backend(ABC):

    def __init__(self, width, height, publish_recording_status_func):
        self.width = width
        self.height = height
        self.publish_recording_status_func = publish_recording_status_func

        self.recording = False
        self.recording_output_file = None
        self.recording_start_time = None

        # time that we last called self.send_recording_status
        self.prev_recording_status_time = 0
        # Time between recording statuses, in seconds
        self.recording_status_interval = 60

    def start_video(self):
        pass

    def on_base_overlay_update(self, base_canvas: Canvas):
        pass

    def on_overlays_updated(self, data_canvas: Canvas, message_canvas: Canvas):
        pass

    def on_loop(self):
        """ Executes all operations that should run every iteration of the
            Overlay loop.

            This includes sending the recording status (if it is due) and
            depending on the backend, the display may be updated during this
            call. This operation may be blocking to ensure the display is
            updated at the correct framerate. """
        self._on_loop()

        if time() > self.prev_recording_status_time + self.recording_status_interval:
            self.send_recording_status()

    def _on_loop(self):
        pass

    def stop_video(self):
        pass

    def start_recording(self):
        """ Starts an h264 recording with the first available name located in
            the recordings folder.

            Should be paired with a call to stop_recording."""

        output_folder = path.dirname(path.realpath(__file__)) + "../recordings"
        output_file_pattern = f"{output_folder}/rec_{{}}.h264"

        if not path.exists(output_folder):
            mkdir(output_folder)

        video_number = 1
        while path.exists(output_file_pattern.format(video_number)):
            video_number += 1
        self.recording_output_file = output_file_pattern.format(video_number)

        self.__start_recording()

    def _start_recording(self):
        print(f"WARNING: Recording is not supported with {type(self).__name__}")

    def stop_recording(self):
        """ Stops and saves any current recording at the location found in
            self.recording_output_file.

            Should be paired with a call to start_recording. No action is taken
            if there was no recording in progress. """

        print(f"WARNING: Recording is not supported with {type(self).__name__}")

    def check_recording_errors(self):
        """ Check if any errors have occured during recording, and if any have
            occured, throw exceptions. """

    def send_recording_status(self):
        """ Checks if any errors have occured with recording, and sends the
            current recording status via MQTT """

        message = {}

        if self.recording:
            try:
                self.check_recording_errors()
                message["status"] = "recording"
                message["recordingMinutes"] = (time() - self.recording_start_time) / 60
                message["recordingFile"] = self.recording_output_file

            except Exception:
                self.send_recording_error()
                return
        else:
            message["status"] = "off"
        _, _, free_disk_space = disk_usage(__file__)
        message["diskSpaceRemaining"] = free_disk_space

        self.publish_recording_status_func(dumps(message))
        self.prev_recording_status_time = time()

    def send_recording_error(self):
        """ Sends the most recent exception to the recording status MQTT topic """

        _, _, free_disk_space = disk_usage(__file__)
        message = {
            "status": "error",
            "error": format_exc(),
            "diskSpaceRemaining": free_disk_space,
        }
        self.publish_recording_status_func(dumps(message))
        print(format_exc())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_video()
