from abc import ABC, abstractmethod

from overlay import Overlay, Canvas, Colour
from data import Data

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

    def __init__(self, title, data_key, coordinate):
        self.title = title
        self.data_key = data_key
        self.title_coord = (coordinate[0] + DataField.width, coordinate[1] - DataField.spacing - DataField.data_height)
        self.data_coord = (coordinate[0] + DataField.width, coordinate[1])

    def draw_base(self, canvas: Canvas):
        canvas.draw_text(self.title, self.title_coord, size=0.8, colour=Colour.white, align="right")

    def draw_data(self, canvas: Canvas, data: Data):
        value = str(data[self.data_key])
        value = "101.2"
        canvas.draw_text(value, self.data_coord, size=1.5, colour=Colour.white, align="right")

class OverlayNew(Overlay):

    def __init__(self, bike=None):
        super(OverlayNew, self).__init__(bike)

        spacing = 20
        first_row_y = self.height - (2 * spacing + DataField.height)
        second_row_y = self.height - spacing
        self.drawables = [
            DataField("GPS KPH", "gps_speed", (spacing, first_row_y)),
            DataField("TIME", "time", (spacing, second_row_y)),
        ]

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with rc: {}'.format(rc))

        for drawable in self.drawables:
            drawable.draw_base(self.base_canvas)

    def update_data_layer(self):
        self.data_canvas.clear()

        for drawable in self.drawables:
            drawable.draw_data(self.data_canvas, self.data)

if __name__ == '__main__':
    args = Overlay.get_overlay_args("An empty, example overlay")
    my_overlay = OverlayNew(args.bike)
    my_overlay.connect(ip=args.host)
