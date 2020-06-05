from abc import ABC, abstractmethod
from json import dumps
from pathlib import Path
from shutil import disk_usage
from time import time
from traceback import format_exc
from typing import Callable

from canvas import Canvas

# A function which accepts a string and returns None
PublishFunc = Callable[[str], None]

class Backend(ABC):
    """ Backend for getting and processing video feed.

        Handles combining the video feed with overlays and displaying, and
        recording the video feed to a file. """

    def __init__(self, width: int, height: int, publish_recording_status_func: PublishFunc):
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

    @abstractmethod
    def start_video(self) -> None:
        """ Starts the necessary processes to begin displaying camera feed
            video. """

    @abstractmethod
    def on_base_canvas_updated(self, base_canvas: Canvas) -> None:
        """ Updates the base canvas which is drawn on the video. Should be
            called whenever the canvas is updated. """

    @abstractmethod
    def on_canvases_updated(self, data_canvas: Canvas, message_canvas: Canvas) -> None:
        """ Updates the data and message canvases which are drawn on the
            video. Should be called whenever the canvases are updated. """

    def on_loop(self) -> None:
        """ Executes all operations that should run every iteration of the
            Overlay loop.

            This includes sending the recording status (if it is due) and
            depending on the backend, the display may be updated during this
            call. This operation may be blocking to ensure the display is
            updated at the correct framerate. """

        self._on_loop()

        if time() > self.prev_recording_status_time + self.recording_status_interval:
            self.send_recording_status()

    @abstractmethod
    def _on_loop(self) -> None:
        """ Implemented by overlays to perform any neccessary operations that
            should be performed on a regular period. This may involve updating
            the display, which may be blocking. Should not be called outside
            of the Backend class. """

    @abstractmethod
    def stop_video(self) -> None:
        """ Stops displaying the video feed and releases any resources
            captured. """

    def start_recording(self) -> None:
        """ Starts an h264 recording with the first available name located in
            the recordings folder.

            Should be paired with a call to stop_recording."""

        # Ensure output folder exists
        output_folder = Path(__file__).parent.parent / "recordings"
        output_folder.mkdir(exist_ok=True)

        # Find next available video filename
        video_number = 1
        output_file_pattern = "rec_{}.h264"
        while (output_folder / output_file_pattern.format(video_number)).exists():
            video_number += 1
        self.recording_output_file = str(output_folder / output_file_pattern.format(video_number))

        self._start_recording()

    def _start_recording(self) -> None:
        """ Starts recording to the file at self.recording_output_file. Should
            not be called outside of the Backend class. """

        raise NotImplementedError(f"Recording is not supported with {type(self).__name__}")

    def stop_recording(self) -> None:
        """ Stops and saves any current recording at the location found in
            self.recording_output_file.

            Should be paired with a call to start_recording. No action is taken
            if there was no recording in progress. """

        raise NotImplementedError(f"Recording is not supported with {type(self).__name__}")

    def check_recording_errors(self) -> None:
        """ Check if any errors have occured during recording, and if any have
            occured, throw exceptions. """

    def send_recording_status(self) -> None:
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

    def send_recording_error(self) -> None:
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
        """ Ran when Python's `with ...` syntax is used on an instance of this
            class. """
        self.start_video()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ Ran when exiting a `with` block. """
        self.stop_video()
