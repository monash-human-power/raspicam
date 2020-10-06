from components import Component
from canvas import Canvas, Colour
from data import Data

class Translucent(Component):
    """A translucent rectangle behind the data overlay for data values to stand out
    from a white background (white racetrack, lines, etc).
    """
    TOP_LEFT_COORDS = (0, 570)
    BOTTOM_RIGHT_COORDS = (1280, 740)
    COLOUR = Colour.blue

    def draw_base(self, canvas: Canvas):
        canvas.draw_rect(
            Translucent.TOP_LEFT_COORDS,
            Translucent.BOTTOM_RIGHT_COORDS,
            Translucent.COLOUR
        )

    def draw_data(self, canvas: Canvas, data: Data):
        pass