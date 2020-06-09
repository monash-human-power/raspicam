from abc import ABC, abstractmethod
from time import time

from overlay import Overlay, Canvas, Colour
from data import Data
from typing import Callable, Tuple

class Drawable(ABC):
    @abstractmethod
    def draw_base(self, canvas: Canvas):
        pass
    @abstractmethod
    def draw_data(self, canvas: Canvas, data: Data):
        pass

class DataField(Drawable):

    width = 137

    title_height = 18
    data_height = 32
    spacing = 10

    height = title_height + data_height + spacing

    def __init__(self, title: str, value_func: Callable[[], str], coordinate: Tuple[int, int]):
        self.title = title
        self.value_func = value_func
        self.title_coord = (coordinate[0] + DataField.width, coordinate[1] - DataField.spacing - DataField.data_height)
        self.data_coord = (coordinate[0] + DataField.width, coordinate[1])

    def draw_base(self, canvas: Canvas):
        canvas.draw_text(self.title, self.title_coord, size=0.8, colour=Colour.white, align="right")

    def draw_data(self, canvas: Canvas, data: Data):
        canvas.draw_text(self.value_func(), self.data_coord, size=1.5, colour=Colour.white, align="right")

class OverlayNew(Overlay):

    def __init__(self, bike=None):
        super(OverlayNew, self).__init__(bike)

        self.start_time = time()

        spacing = 20
        first_row_y = self.height - (2 * spacing + DataField.height)
        second_row_y = self.height - spacing
        self.drawables = [
            DataField("GPS KPH", self.get_data_func("gps_speed", 1), (spacing, first_row_y)),
            DataField("TIME", self.time_func, (spacing, second_row_y)),
        ]

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with rc: {}'.format(rc))

        for drawable in self.drawables:
            drawable.draw_base(self.base_canvas)

    def update_data_layer(self):
        self.data_canvas.clear()

        for drawable in self.drawables:
            drawable.draw_data(self.data_canvas, self.data)

    def get_data_func(self, data_key: str, decimals=0) -> Callable[[], str]:
        """ Returns a lambda function which, when called, returns the current
            value for the data field `data_key` formatted to `decimals` decimal
            places. """
        format_str = f"{{:.{decimals}f}}"
        return lambda: format_str.format(self.data[data_key])

    def time_func(self) -> str:
        """ Returns the time since the overlay was initialised formatted mm:ss """
        _, rem = divmod(time() - self.start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}:{:0>2}".format(int(minutes), int(seconds))

if __name__ == '__main__':
    args = Overlay.get_overlay_args("An empty, example overlay")
    my_overlay = OverlayNew(args.bike)
    my_overlay.connect(ip=args.host)
