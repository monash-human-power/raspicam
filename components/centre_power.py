from canvas import Canvas, Colour
from components import Component
from data import Data

class CentrePower(Component):
    """ Displays the current and recommended power at the bottom-centre of the
        screen.

        If the current power is within 5% of recommended, it is coloured green,
        otherwise red. If no recommended power is available, it is coloured
        black. """

    power_size = 2.5
    rec_power_size = 1.5
    _, rec_power_height = Canvas.get_text_dimensions("500w", rec_power_size)
    spacing = 10

    power_tolerance = 0.05

    def __init__(self, screen_w: int, screen_h: int):
        self.power_coord = (screen_w // 2, screen_h - 30 - CentrePower.spacing - CentrePower.rec_power_height)
        self.rec_power_coord = (screen_w // 2, screen_h - 30)

    def draw_base(self, canvas: Canvas):
        pass

    def draw_data(self, canvas: Canvas, data: Data):
        power = data["power"]
        rec_power = data["rec_power"]

        power_str = f"{power:.0f}w"
        rec_power_str = f"{rec_power:.0f}w rec"

        if rec_power == 0:
            power_colour = Colour.black
        else:
            power_diff = abs(power / rec_power - 1)
            # Colour.green is too light against the white fairing
            dark_green = (0, 191, 0, 255)
            power_colour = dark_green if power_diff <= CentrePower.power_tolerance else Colour.red

        canvas.draw_text(power_str, self.power_coord, CentrePower.power_size, power_colour, "centre")
        canvas.draw_text(rec_power_str, self.rec_power_coord, CentrePower.rec_power_size, Colour.black, "centre")
