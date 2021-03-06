from components import (
    TransparentRectangle,
    DataField,
    SpeedField,
    CentrePower,
    DAShboardMessage,
    DASDisconnectMessage,
)
from overlay import Overlay


class OverlayNew(Overlay):
    def __init__(self, bike=None, bg=None):
        super().__init__(bike, bg=bg)

        # Generate coordinates for each of the data fields in the
        # bottom corners.
        # Note: These coordinates are for the bottom left corner of each field.
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

        def data_field_coord(x, y):
            """Coordinates of the data field in column x, row y."""
            return col_coords[x], row_coords[y]

        # Dimensions of the left TransparentRectangle
        left_rect = [
            (0, row_coords[0] - DataField.height - spacing),
            (col_coords[1] + DataField.width + spacing, self.height),
        ]

        # Dimensions of the right TransparentRectangle
        right_rect = [
            (col_coords[2], row_coords[0] - DataField.height - spacing),
            (self.width, self.height),
        ]

        # Create all overlay components
        self.components = [
            TransparentRectangle(*left_rect),
            TransparentRectangle(*right_rect),
            DataField(
                "RPM", self.get_data_func("cadence"), data_field_coord(0, 0)
            ),
            DataField(
                "BPM", self.get_data_func("heartRate"), data_field_coord(0, 1)
            ),
            SpeedField(data_field_coord(1, 0)),
            DataField("TIME", self.time_func, data_field_coord(1, 1)),
            DataField(
                "REC KPH",
                self.get_data_func("rec_speed", 1),
                data_field_coord(2, 0),
            ),
            DataField(
                "ZONE KM",
                self.get_data_func("zdist", 2, 0.001),
                data_field_coord(2, 1),
            ),
            DataField(
                "MAX KPH",
                self.get_data_func("predicted_max_speed", 1),
                data_field_coord(3, 0),
            ),
            DataField(
                "DIST KM",
                self.get_data_func("reed_distance", 2, 0.001),
                data_field_coord(3, 1),
            ),
            CentrePower(self.width, self.height),
            DAShboardMessage(),
            DASDisconnectMessage(self.client),
        ]

    def _draw_base_layer(self):
        for component in self.components:
            component.draw_base(self.base_canvas)

    def _update_data_layer(self):
        self.data_canvas.clear()

        for component in self.components:
            component.draw_data(self.data_canvas, self.data)


if __name__ == "__main__":
    args = Overlay.get_overlay_args("An empty, example overlay")
    my_overlay = OverlayNew(args.bike, args.bg)
    my_overlay.connect(ip=args.host)
