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
    # Set height tall enough to fit the largest expected string
    _, rec_power_height = Canvas.get_text_dimensions("500w", rec_power_size)
    spacing = 10

    power_tolerance = 0.05

    def __init__(self, screen_w: int, screen_h: int):
        self.power_coord = (
            screen_w // 2,
            screen_h - 30 - CentrePower.spacing - CentrePower.rec_power_height,
        )
        self.rec_power_coord = (screen_w // 2, screen_h - 30)

    def draw_base(self, canvas: Canvas):
        pass

    def draw_data(self, canvas: Canvas, data: Data):
        power = data["power"].get()
        rec_power = data["rec_power"].get()

        if data["power"].is_valid():
            power_str = data["power"].get_string() + "w"
        else:
            power_str = "--"
        if data["rec_power"].is_valid():
            rec_power_str = data["rec_power"].get_string() + "w rec"
        else:
            rec_power_str = "--"

        if rec_power == 0 or rec_power is None or power is None:
            rec_power_colour = Colour.white
        else:
            power_diff = abs(power / rec_power - 1)
            # Colour.green is too light against the white fairing
            dark_green = (0, 191, 0, 255)
            rec_power_colour = (
                dark_green
                if power_diff <= CentrePower.power_tolerance
                else Colour.red
            )

        canvas.draw_text(
            power_str,
            self.power_coord,
            CentrePower.power_size,
            Colour.white,
            "centre",
        )
        canvas.draw_text(
            rec_power_str,
            self.rec_power_coord,
            CentrePower.rec_power_size,
            rec_power_colour,
            "centre",
        )
