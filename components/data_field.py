from typing import Callable, Tuple
from canvas import Canvas, Colour
from components import Component
from data import Data


class DataField(Component):
    """ A simple data field containing a large value below a title in a smaller
        font. Text is right-aligned. """

    title_size = 0.8
    data_size = 1.5

    # Set widths and heights large enough to fit the largest expected strings
    width, data_height = Canvas.get_text_dimensions("00:00", data_size)
    _, title_height = Canvas.get_text_dimensions("KPH", title_size)

    spacing = 10

    height = title_height + data_height + spacing

    def __init__(
        self,
        title: str,
        value_func: Callable[[Data], str],
        coordinate: Tuple[int, int],
        is_title_static: bool = True,
    ):
        """Constructor for a DataField component.

        `coordinate` specifies the bottom-left coordinate of the data field.
        """
        self.title = title
        self.is_title_static = is_title_static
        self.value_func = value_func
        self.title_coord = (
            coordinate[0] + DataField.width,
            coordinate[1] - DataField.spacing - DataField.data_height,
        )
        self.data_coord = (coordinate[0] + DataField.width, coordinate[1])

    def draw_base(self, canvas: Canvas):
        canvas.draw_text(
            self.title,
            self.title_coord,
            DataField.title_size,
            Colour.white,
            "right",
        )

    def draw_data(self, canvas: Canvas, data: Data):
        if not self.is_title_static:
            DataField.draw_base(self, canvas)
        canvas.draw_text(
            self.value_func(data),
            self.data_coord,
            DataField.data_size,
            Colour.white,
            "right",
        )


class SpeedField(DataField):
    """ A specialised version of DataField which prefers to display GPS velocity,
        but falls back to reed or ANT+ speed if GPS velocity is unavailable """

    def get_data_source(data: Data) -> str or None:
        priority_list = ["gps_speed", "reed_velocity", "ant_speed"]
        for source in priority_list:
            if data[source].get() is not None:
                return source
        return None

    def __init__(self, coordinate: Tuple[int, int]):
        def value_func(data):
            source = SpeedField.get_data_source(data)
            if source is None:
                return "--"
            return data[source].get_string(decimals=1)

        super().__init__("", value_func, coordinate, False)

    def draw_base(self, canvas: Canvas):
        pass

    def draw_data(self, canvas: Canvas, data: Data):
        source = SpeedField.get_data_source(data)
        titles = {
            "gps_speed": "GPS KPH",
            "ant_speed": "ANT+ KPH",
            "reed_velocity": "REED KPH",
            None: "KPH",
        }
        self.title = titles[source]
        super().draw_data(canvas, data)


class VoltageField(DataField):
    """ A specialised version of DataField which displays the voltage adjusting
        for it's values whether the battery is low, medium or high."""

    def __init__(
        self,
        title: str,
        value_func: Callable[[Data], str],
        coordinate: Tuple[int, int],
        is_title_static: bool = True,
    ):
        super().__init__(title, value_func, coordinate, is_title_static)

    def draw_base(self, canvas: Canvas):
        return super().draw_base(canvas)

    def draw_data(self, canvas: Canvas, data: Data):
        if not self.is_title_static:
            DataField.draw_base(self, canvas)
        voltage_value = self.value_func(data)
        if voltage_value == "--" or float(voltage_value) >= 7.3:
            colour = Colour.white
        elif float(voltage_value) >= 7.0:
            colour = Colour.yellow
        else:
            colour = Colour.red
        canvas.draw_text(
            voltage_value,
            self.data_coord,
            DataField.data_size * 0.7,
            colour,
            "right",
        )
