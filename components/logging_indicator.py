from components import Component
from canvas import Canvas, Colour, Coord
from data import Data


class LoggingIndicator(Component):
    """A red circle to symbolise DAS logging"""

    COLOUR = Colour.red
    RADIUS = 10

    def __init__(self, center: Coord):
        self.center = center

    def draw_base(self, canvas: Canvas):
        pass

    def draw_data(self, canvas: Canvas, data: Data):
        if data.is_logging():
            # canvas.draw_circle(
            #     self.center, LoggingIndicator.RADIUS, LoggingIndicator.COLOUR
            # )
            pass # Never shows logging indicator
