from abc import ABC, abstractmethod
from time import time

from canvas import Canvas, Colour
from data import Data
from overlay import Overlay
from typing import Callable, Tuple

class Drawable(ABC):
    @abstractmethod
    def draw_base(self, canvas: Canvas):
        pass
    @abstractmethod
    def draw_data(self, canvas: Canvas, data: Data):
        pass

class DataField(Drawable):

    title_size = 0.8
    data_size = 1.5

    width, data_height = Canvas.get_text_dimensions("100.0", data_size)
    _, title_height = Canvas.get_text_dimensions("KPH", title_size)

    spacing = 10

    height = title_height + data_height + spacing

    def __init__(self, title: str, value_func: Callable[[], str], coordinate: Tuple[int, int]):
        """ `coordinate` specifies the bottom-left coordinate of the data field. """
        self.title = title
        self.value_func = value_func
        self.title_coord = (coordinate[0] + DataField.width, coordinate[1] - DataField.spacing - DataField.data_height)
        self.data_coord = (coordinate[0] + DataField.width, coordinate[1])

    def draw_base(self, canvas: Canvas):
        canvas.draw_text(self.title, self.title_coord, size=DataField.title_size, colour=Colour.white, align="right")

    def draw_data(self, canvas: Canvas, data: Data):
        canvas.draw_text(self.value_func(), self.data_coord, size=DataField.data_size, colour=Colour.white, align="right")

class CentrePower(Drawable):

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
            # Colour.green is to light against the white fairing
            dark_green = (0, 191, 0, 255)
            power_colour = dark_green if power_diff <= CentrePower.power_tolerance else Colour.red

        canvas.draw_text(power_str, self.power_coord, CentrePower.power_size, power_colour, "centre")
        canvas.draw_text(rec_power_str, self.rec_power_coord, CentrePower.rec_power_size, Colour.black, "centre")

class OverlayNew(Overlay):

    def __init__(self, bike=None):
        super(OverlayNew, self).__init__(bike)

        self.start_time = time()

        spacing = 20
        row_coords = [
            self.height - (2 * spacing + DataField.height),
            self.height - spacing,
        ]
        col_coords = [
            spacing,
            2 * spacing + DataField.width,
            self.width - 2 * (spacing + DataField.width),
            self.width - (spacing + DataField.width),
        ]
        data_field_coord = lambda x, y: (col_coords[x], row_coords[y])
        self.drawables = [
            DataField("GPS KPH", self.get_data_func("gps_speed", 1), data_field_coord(0, 0)),
            DataField("TIME", self.time_func, data_field_coord(0, 1)),
            DataField("RPM", self.get_data_func("cadence"), data_field_coord(1, 0)),
            DataField("BPM", self.get_data_func("heartRate"), data_field_coord(1, 1)),

            DataField("REC KPH", self.get_data_func("rec_speed", 1), data_field_coord(2, 0)),
            DataField("ZONE KM", self.get_data_func("zdist", 2, 0.001), data_field_coord(2, 1)),
            DataField("MAX KPH", self.get_data_func("predicted_max_speed", 1), data_field_coord(3, 0)),
            DataField("DIST KM", self.get_data_func("reed_distance", 2, 0.001), data_field_coord(3, 1)),

            CentrePower(self.width, self.height),
        ]

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with rc: {}'.format(rc))

        for drawable in self.drawables:
            drawable.draw_base(self.base_canvas)

    def update_data_layer(self):
        self.data_canvas.clear()

        for drawable in self.drawables:
            drawable.draw_data(self.data_canvas, self.data)

    def get_data_func(self, data_key: str, decimals=0, scalar=1) -> Callable[[], str]:
        """ Returns a lambda function which, when called, returns the current
            value for the data field `data_key`, multiplied by `scalar`, and
            formatted to `decimals` decimal places. """
        format_str = f"{{:.{decimals}f}}"
        return lambda: format_str.format(self.data[data_key] * scalar)

    def time_func(self) -> str:
        """ Returns the time since the overlay was initialised formatted mm:ss """
        _, rem = divmod(time() - self.start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}:{:0>2}".format(int(minutes), int(seconds))

if __name__ == '__main__':
    args = Overlay.get_overlay_args("An empty, example overlay")
    my_overlay = OverlayNew(args.bike)
    my_overlay.connect(ip=args.host)
