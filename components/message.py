from textwrap import wrap

from canvas import Canvas
from components import Component
from data import Data


class Message(Component):
    """ Displays any existing messages at the top of the screen.

        Lines are wrapped appropriately to ensure the entire message is
        visible. """

    text_size = 1
    spacing = 10
    # Set height tall enough to fit the largest expected string
    _, text_height = Canvas.get_text_dimensions("blah", text_size)
    chars_per_line = 75

    def draw_base(self, canvas: Canvas):
        pass

    def draw_data(self, canvas: Canvas, data: Data):
        if not data.has_message():
            return
        message = data.get_message()
        display_str = f"Message: {message}"

        # Display each line of the message
        line_y_coord = Message.spacing + Message.text_height
        for line in wrap(display_str, Message.chars_per_line):
            coord = (Message.spacing, line_y_coord)
            canvas.draw_text(line, coord, Message.text_size)
            line_y_coord += Message.text_height + Message.spacing
