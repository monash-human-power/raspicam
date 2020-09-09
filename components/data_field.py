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
    """ A specialised version of DataField which prefers to display GPS speed,
        but falls back to reed velocity if GPS is unavailable """

    def __init__(self, coordinate: Tuple[int, int]):
        def value_func(data):
            data_string = data["gps_speed"].get_string(1) or data["reed_velocity"].get_string(1)
            if data_string is not None:
                return data_string
            else:
                return "--"

        super().__init__("", value_func, coordinate, False)

    def draw_base(self, canvas: Canvas):
        pass

    def draw_data(self, canvas: Canvas, data: Data):
        self.title = "GPS KPH" if data["gps_speed"] else "REED KPH"
        super().draw_data(canvas, data)
