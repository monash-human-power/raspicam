import time
from overlay import Overlay
from canvas import Colour


class OverlayTopStrip(Overlay):
    def __init__(self, bike=None, bg=None):
        super(OverlayTopStrip, self).__init__(bike, bg=bg)

        self.start_time = round(time.time(), 2)

        self.bottom_text_height = 70
        self.bottom_text_pos_x = self.width // 2 - 150
        self.bottom_text_pos_y = self.height - 8
        self.bottom_text_size = 2.2
        self.top_box_height = 60
        self.top_box_width = self.width
        self.top_text_pos = self.top_box_height - 15

    def _draw_base_layer(self):
        self.base_canvas.draw_rect(
            (0, 0), (self.top_box_width, self.top_box_height)
        )
        self.base_canvas.draw_text(
            "T:", (0, self.top_text_pos), colour=Colour.white
        )
        self.base_canvas.draw_text(
            "ZDL:", (256, self.top_text_pos), colour=Colour.white
        )
        self.base_canvas.draw_text(
            "RP:", (512, self.top_text_pos), colour=Colour.white
        )
        self.base_canvas.draw_text(
            "PMV:", (768, self.top_text_pos), colour=Colour.white
        )
        self.base_canvas.draw_text(
            "MS:", (1024, self.top_text_pos), colour=Colour.white
        )

    def _update_data_layer(self):
        # Create a transparent image to attach text
        self.data_canvas.clear()

        # Display elapsed time:
        _, rem = divmod(time.time() - self.start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        time_string = "{:0>2}:{:0>2}".format(int(minutes), int(seconds))
        self.data_canvas.draw_text(
            time_string, (50, self.top_text_pos), colour=Colour.white
        )

        if self.data["power"].get() != 0:
            self.draw_power_rec_power()

        if self.data["gps"].get() == 1:
            if self.data["gps_speed"] != 0:
                self.draw_speed_max_speed()

        # Display zone distance left (bugged)
        if self.data["zdist"].get() != 0:
            self.draw_zone_dist()

        # Display plan name and clear after 15 secs
        if (
            self.data["plan_name"].get() != ""
            and time.time() - self.start_time <= 15
        ):
            self.draw_plan_name()

    def draw_power_rec_power(self):
        power = self.data["power"].get()
        rec_power = self.data["rec_power"].get()
        # Display recommended power
        if self.data["rec_power"].is_valid():
            rec_power_text = "{0}".format(round(rec_power, 0))
        else:
            rec_power_text = "--"
        self.data_canvas.draw_text(
            rec_power_text, (600, self.top_text_pos), colour=Colour.white,
        )

        # Display power (no colour change)
        if self.data["power"].is_valid():
            power_text = "P: {0}".format(round(power, 2))
        else:
            power_text = "--"
        self.data_canvas.draw_text(
            power_text,
            (self.bottom_text_pos_x, self.bottom_text_pos_y),
            size=self.bottom_text_size,
            colour=Colour.red,
        )

    def draw_speed_max_speed(self):
        # Predicted max speed
        pred_max_speed = self.data["predicted_max_speed"].get()
        if self.data["predicted_max_speed"].is_valid():
            max_speed_text = "{0}".format(round(pred_max_speed, 1))
        else:
            max_speed_text = "--"
        self.data_canvas.draw_text(
            max_speed_text, (890, self.top_text_pos), colour=Colour.white,
        )

        # Actual speed (no colour change)
        speed = self.data["gps_speed"].get()
        if self.data["gps_speed"].is_valid():
            speed_text = "{0}".format(int(speed))
        else:
            speed_text = "--"
        self.data_canvas.draw_text(
            "S: {0}".format(round(speed, 2)),
            (
                self.bottom_text_pos_x,
                self.bottom_text_pos_y - self.bottom_text_height,
            ),
            size=self.bottom_text_size,
            colour=Colour.red,
        )
        self.data_canvas.draw_text(
            speed_text, (1120, self.top_text_pos), colour=Colour.white,
        )

    def draw_zone_dist(self):
        zdist_left = self.data["zdist"].get()
        if self.data["zdist"].is_valid():
            zdist_left_text = "{0}".format(int(zdist_left))
        else:
            zdist_left_text = "--"
        self.data_canvas.draw_text(
            zdist_left_text, (360, self.top_text_pos), colour=Colour.white,
        )

    def draw_plan_name(self):
        plan_name = self.data["plan_name"].get_string()
        self.data_canvas.draw_text(
            plan_name, (0, self.height - 8), colour=Colour.red
        )


if __name__ == "__main__":
    args = Overlay.get_overlay_args(
        "Shows important statistics in a bar at the top of the screen"
    )
    my_overlay = OverlayTopStrip(args.bike, args.bg)
    my_overlay.connect(ip=args.host)
