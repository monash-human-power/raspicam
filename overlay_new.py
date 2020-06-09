from abc import ABC, abstractmethod

from overlay import Overlay, Canvas, Colour
from data import Data

class Drawable(ABC):
    @abstractmethod
    def drawBase(self, canvas: Canvas):
        pass
    @abstractmethod
    def drawData(self, canvas: Canvas, data: Data):
        pass

class DataField(Drawable):
    def __init__(self, title, data_key, coordinate):
        self.title = title
        self.data_key = data_key
        self.coord = coordinate

    def drawBase(self, canvas: Canvas):
        canvas.draw_text(self.title, self.coord, size=1, colour=Colour.white)

    def drawData(self, canvas: Canvas, data: Data):
        value = str(data[self.data_key])
        canvas.draw_text(value, self.coord, size=1.5, colour=Colour.white)

class OverlayNew(Overlay):

    def __init__(self, bike=None):
        super(OverlayNew, self).__init__(bike)

        self.drawables = [
            DataField("KPH", "gps_speed", (10, 10)),
        ]

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with rc: {}'.format(rc))

        for drawable in self.drawables:
            drawable.drawBase(self.base_canvas)

    def update_data_layer(self):
        self.data_canvas.clear()

        for drawable in self.drawables:
            drawable.drawData(self.data_canvas, self.data)

if __name__ == '__main__':
    args = Overlay.get_overlay_args("An empty, example overlay")
    my_overlay = OverlayNew(args.bike)
    my_overlay.connect(ip=args.host)
