from components import Component
from canvas import Canvas, Colour, Coord
from data import Data


class Transparent(Component):
    """A transparent rectangle behind the data overlay for data values to stand out
    from a white background (white racetrack, lines, etc).
    """

    COLOUR = Colour.transparentBlack

    def __init__(self, top_left_coords: Coord, bottom_right_coords: Coord):
        self.top_left_coords = top_left_coords
        self.bottom_right_coords = bottom_right_coords

    def draw_base(self, canvas: Canvas):
        canvas.draw_rect(
            self.top_left_coords, self.bottom_right_coords, Transparent.COLOUR
        )

    def draw_data(self, canvas: Canvas, data: Data):
        pass
