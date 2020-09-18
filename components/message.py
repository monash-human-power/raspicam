from textwrap import wrap
from abc import ABC, abstractmethod

from canvas import Canvas, Colour
from components import Component
from data import Data


class Message(Component, ABC):
    """Abstract class for messages to display on the camera overlay.

    Lines are wrapped appropriately to ensure the entire message is
    visible.
    
    Attributes:
        text_size: Integer for the text size on Canvas
        spacing: Integer for the spacing between lines of text
        text_height: Integer for the height of a line of text
        chars_per_line: Integer representing the number of characters per line
    """

    text_size = 1
    spacing = 10
    # Set height tall enough to fit the largest expected string
    _, text_height = Canvas.get_text_dimensions("blah", text_size)
    chars_per_line = 75

    def draw_base(self, canvas: Canvas):
        pass

    @abstractmethod
    def draw_data(self, canvas: Canvas, data: Data):
        pass

    def _display_message(
        self, canvas: Canvas, message: str, colour: Colour = Colour.black
    ):
        """Display message on data overlay by wrapping each line starting
        from the top."""

        line_y_coord = Message.spacing + Message.text_height
        for line in wrap(message, Message.chars_per_line):
            coord = (Message.spacing, line_y_coord)
            canvas.draw_text(line, coord, Message.text_size, colour)
            line_y_coord += Message.text_height + Message.spacing
