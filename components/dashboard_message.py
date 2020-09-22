from components import Message
from canvas import Canvas
from data import Data


class DAShboardMessage(Message):
    """Displays messages sent from the DAShboard onto the camera overlay.

    Messages can only be received when the overlay is connected to the DAS.
    """

    def draw_data(self, canvas: Canvas, data: Data) -> None:
        if not data.has_message():
            return
        message = data.get_message()
        display_str = f"Message: {message}"
        self._display_message(canvas, display_str)
