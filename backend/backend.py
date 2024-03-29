from abc import ABC, abstractmethod
from json import dumps
from pathlib import Path
from shutil import disk_usage
from time import time
from traceback import format_exc
from typing import Callable

from canvas import Canvas
from config import ROTATION_KEY, read_configs

# A function which accepts a string and returns None
PublishFunc = Callable[[str], None]


class Backend(ABC):
    """ Backend for getting and processing video feed.

        Handle combining the video feed with overlays and displaying, and
        recording the video feed to a file. """

    def __init__(
        self,
        width: int,
        height: int,
        publish_recording_status_func: PublishFunc,
        publish_video_status_func: PublishFunc,
        exception_handler: PublishFunc,
    ):
        self.width = width
        self.height = height
        self.publish_recording_status_func = publish_recording_status_func
        self.publish_video_status_func = publish_video_status_func
        self.exception_handler = exception_handler

        self.recording = False
        self.recording_output_file = None
        self.recording_start_time = None

        # Time that we last called self.send_recording_status
        self.prev_record_status_time = 0
        # Time between recording statuses, in seconds
        self.record_status_interval = 60

        # Time that we last called self.send_video_status
        self.prev_video_status_time = 0
        # Time between recording statuses, in seconds
        self.video_status_interval = 60

        # Rotation of video feed in degrees clockwise
        self.video_rotation = read_configs().get(ROTATION_KEY, 0)

    @abstractmethod
    def _is_video_on(self) -> bool:
        """ Check if the video feed is running.

        Returns:
            bool: True if is on, False otherwise
        """

    @abstractmethod
    def start_video(self) -> None:
        """ Start the necessary processes to begin displaying camera feed
            video. """

    def on_base_canvas_updated(self, base_canvas: Canvas) -> None:
        """ Update the base layer of the overlay whenever the canvas is updated,
            which is shown on the camera.

            Catches any errors that occurs while the base canvas is being
            updated. """
        with self.exception_handler:
            self._on_base_canvas_updated(base_canvas)

    @abstractmethod
    def _on_base_canvas_updated(self, base_canvas: Canvas) -> None:
        """ Update the base canvas which is drawn on the video. Should be
            called whenever the canvas is updated. """

    def on_canvases_updated(
        self, data_canvas: Canvas, message_canvas: Canvas
    ) -> None:
        """ Update the data and message layers of the overlay whenever the canvas
            is updated, which is shown on the camera.

            Catches any errors that occurs while either the data or message
            canvas is being updated. """
        with self.exception_handler:
            self._on_canvases_updated(data_canvas, message_canvas)

    @abstractmethod
    def _on_canvases_updated(
        self, data_canvas: Canvas, message_canvas: Canvas
    ) -> None:
        """ Update the data and message canvases which are drawn on the
            video. Should be called whenever the canvases are updated. """

    def on_loop(self) -> None:
        """ Execute all operations that should run every iteration of the
            Overlay loop.

            This includes sending the recording status (if it is due) and
            depending on the backend, the display may be updated during this
            call. This operation may be blocking to ensure the display is
            updated at the correct framerate. """
        with self.exception_handler:
            self._on_loop()

        if time() > self.prev_record_status_time + self.record_status_interval:
            self.send_recording_status()

        if time() > self.prev_video_status_time + self.video_status_interval:
            self.send_video_status()

    @abstractmethod
    def _on_loop(self) -> None:
        """ Implemented by overlays to perform any necessary operations that
            should be performed on a regular period. This may involve updating
            the display, which may be blocking. Should not be called outside
            of the Backend class. """

    @abstractmethod
    def stop_video(self) -> None:
        """ Stop displaying the video feed and releases any resources
            captured. """

    def start_recording(self) -> None:
        """ Start an h264 recording with the first available name located in
            the recordings folder.

            Should be paired with a call to stop_recording. Does nothing if
            already recording. """

        # If we're already recording just respond with a status
        if self.recording:
            self.send_recording_status()
            return

        # Ensure output folder exists
        output_folder = Path(__file__).parent.parent / "recordings"
        output_folder.mkdir(exist_ok=True)

        # Find next available video filename
        video_number = 1
        output_file_pattern = "rec_{}.h264"
        while (
            output_folder / output_file_pattern.format(video_number)
        ).exists():
            video_number += 1
        self.recording_output_file = str(
            output_folder / output_file_pattern.format(video_number)
        )

        # Start recording. Send an error if one occurs, otherwise a status.
        try:
            self._start_recording()
        except Exception:
            self.recording = False
            self.send_recording_error()
        else:
            self.send_recording_status()

    def _start_recording(self) -> None:
        """ Start recording to the file at self.recording_output_file. Should
            not be called outside of the Backend class. """

        raise NotImplementedError(
            f"Recording is not supported with {type(self).__name__}"
        )

    def stop_recording(self) -> None:
        """ Stop and save any current recording at the location found in
            self.recording_output_file.

            Should be paired with a call to start_recording. No action is taken
            if there was no recording in progress. """

        self.recording = False
        try:
            self._stop_recording()
        except Exception:
            self.send_recording_error()
        else:
            self.send_recording_status()

    def _stop_recording(self) -> None:
        """ Stop recording and save to the file at self.recording_output_file.
            Should not be called outside of the Backend class. """

        raise NotImplementedError(
            f"Recording is not supported with {type(self).__name__}"
        )

    def check_recording_errors(self) -> None:
        """ Check if any errors have occured during recording, and if any have
            occured, throw exceptions. """

    def send_recording_status(self) -> None:
        """ Check if any errors have occured with recording, and sends the
            current recording status via MQTT """

        message = {}

        if self.recording:
            try:
                self.check_recording_errors()
                message["status"] = "recording"
                message["recordingMinutes"] = (
                    time() - self.recording_start_time
                ) / 60
                message["recordingFile"] = self.recording_output_file

            except Exception:
                self.send_recording_error()
                return
        else:
            message["status"] = "off"
        _, _, free_disk_space = disk_usage(Path(__file__).parent)
        message["diskSpaceRemaining"] = free_disk_space

        self.publish_recording_status_func(dumps(message))
        self.prev_record_status_time = time()

    def send_recording_error(self) -> None:
        """Send the most recent exception to the recording status topic."""

        _, _, free_disk_space = disk_usage(Path(__file__).parent)
        message = {
            "status": "error",
            "error": format_exc(),
            "diskSpaceRemaining": free_disk_space,
        }
        self.publish_recording_status_func(dumps(message))
        print(format_exc())

    def send_video_status(self, status: bool = None) -> None:
        """ Publish the camera's status to the camera's online topic. """
        if status is None:
            status = self._is_video_on()
        self.publish_video_status_func(dumps({"online": status}))
        self.prev_video_status_time = time()

    def __enter__(self):
        """ Ran when Python's `with ...` syntax is used on an instance of this
            class. """
        self.start_video()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ Ran when exiting a `with` block. """
        self.stop_video()
        self.send_video_status(False)
