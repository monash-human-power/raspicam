from abc import ABC, abstractmethod
from textwrap import wrap
from time import time
from typing import Callable, Tuple

from canvas import Canvas, Colour
from data import Data
from overlay import Overlay

class Drawable(ABC):
    @abstractmethod
    def draw_base(self, canvas: Canvas):
        pass
    @abstractmethod
    def draw_data(self, canvas: Canvas, data: Data):
        pass

class DataField(Drawable):
    """ A simple data field containing a large value below a title in a smaller
        font. Text is right-aligned. """

    title_size = 0.8
    data_size = 1.5

    width, data_height = Canvas.get_text_dimensions("100.0", data_size)
    _, title_height = Canvas.get_text_dimensions("KPH", title_size)

    spacing = 10

    height = title_height + data_height + spacing

    def __init__(self, title: str, value_func: Callable[[Data], str], coordinate: Tuple[int, int]):
        """ `coordinate` specifies the bottom-left coordinate of the data field. """
        self.title = title
        self.value_func = value_func
        self.title_coord = (coordinate[0] + DataField.width, coordinate[1] - DataField.spacing - DataField.data_height)
        self.data_coord = (coordinate[0] + DataField.width, coordinate[1])

    def draw_base(self, canvas: Canvas):
        canvas.draw_text(self.title, self.title_coord, DataField.title_size, Colour.white, "right")

    def draw_data(self, canvas: Canvas, data: Data):
        canvas.draw_text(self.value_func(data), self.data_coord, DataField.data_size, Colour.white, "right")

class SpeedField(DataField):
    """ A specialised version of DataField which prefers to display GPS speed,
        but falls back to reed velocity if GPS is unavailable """

    def __init__(self, coordinate: Tuple[int, int]):
        value_func = lambda data: "{:.1f}".format(data["gps_speed"] or data["reed_velocity"])
        super().__init__("", value_func, coordinate)

    def draw_base(self, canvas: Canvas):
        pass

    def draw_data(self, canvas: Canvas, data: Data):
        self.title = "GPS KPH" if data["gps_speed"] else "REED KPH"
        super().draw_base(canvas)
        super().draw_data(canvas, data)

class CentrePower(Drawable):
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

class Message(Drawable):
    """ A drawable which displays any existing messages at the top of the
        screen.

        Lines are wrapped appropriately to ensure the entire message is
        visible. """

    text_size = 1
    spacing = 10
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

class OverlayNew(Overlay):

    def __init__(self, bike=None, bg=None):
        super(OverlayNew, self).__init__(bike, bg=bg)

        self.start_time = time()

        # Generate coordinates for each of the data fields in the bottom corners.
        # Note that these coordinates are for the bottom left corner of each field.
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
        # This lambda returns the coordinates of the data field in column x, row y
        data_field_coord = lambda x, y: (col_coords[x], row_coords[y])

        # Create all drawable overlay objects
        self.drawables = [
            SpeedField(data_field_coord(0, 0)),
            DataField("TIME", self.time_func, data_field_coord(0, 1)),
            DataField("RPM", self.get_data_func("cadence"), data_field_coord(1, 0)),
            DataField("BPM", self.get_data_func("heartRate"), data_field_coord(1, 1)),

            DataField("REC KPH", self.get_data_func("rec_speed", 1), data_field_coord(2, 0)),
            DataField("ZONE KM", self.get_data_func("zdist", 2, 0.001), data_field_coord(2, 1)),
            DataField("MAX KPH", self.get_data_func("predicted_max_speed", 1), data_field_coord(3, 0)),
            DataField("DIST KM", self.get_data_func("reed_distance", 2, 0.001), data_field_coord(3, 1)),

            CentrePower(self.width, self.height),

            Message(),
        ]

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with rc: {}'.format(rc))

        for drawable in self.drawables:
            drawable.draw_base(self.base_canvas)

    def update_data_layer(self):
        self.data_canvas.clear()

        for drawable in self.drawables:
            drawable.draw_data(self.data_canvas, self.data)

    def get_data_func(self, data_key: str, decimals=0, scalar=1) -> Callable[[Data], str]:
        """ Returns a lambda function which, when called, returns the current
            value for the data field `data_key`, multiplied by `scalar`, and
            formatted to `decimals` decimal places. """
        format_str = f"{{:.{decimals}f}}"
        return lambda data: format_str.format(data[data_key] * scalar)

    def time_func(self, _: Data) -> str:
        """ Returns the time since the overlay was initialised formatted mm:ss """
        _, rem = divmod(time() - self.start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}:{:0>2}".format(int(minutes), int(seconds))

if __name__ == '__main__':
    args = Overlay.get_overlay_args("An empty, example overlay")
    my_overlay = OverlayNew(args.bike, args.bg)
    my_overlay.connect(ip=args.host)
