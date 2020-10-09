from components import Component
from canvas import Canvas, Colour
from data import Data

class Transparent(Component):
    """A transparent rectangle behind the data overlay for data values to stand out
    from a white background (white racetrack, lines, etc).
    """
    TOP_LEFT_COORDS = (0, 570)
    BOTTOM_RIGHT_COORDS = (1280, 740)
    COLOUR = Colour.blue

    def draw_base(self, canvas: Canvas):
        canvas.draw_rect(
            Transparent.TOP_LEFT_COORDS,
            Transparent.BOTTOM_RIGHT_COORDS,
            Transparent.COLOUR
        )

    def draw_data(self, canvas: Canvas, data: Data):
        pass