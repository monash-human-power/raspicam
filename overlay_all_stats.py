from overlay import Overlay
from canvas import Colour


class OverlayAllStats(Overlay):
    def __init__(self, bike=None, bg=None):
        super(OverlayAllStats, self).__init__(bike, bg=bg)
        self.text_height = 50
        self.speed_height = 70
        self.message_received_time = 0

    def _draw_base_layer(self):
        # Add static text
        self.base_canvas.draw_text("REC Power:", (5, self.text_height * 1))
        self.base_canvas.draw_text("Power:", (5, self.text_height * 2))
        self.base_canvas.draw_text("Cadence:", (5, self.text_height * 3))
        self.base_canvas.draw_text("Distance:", (5, self.text_height * 4))
        self.base_canvas.draw_text("Message:", (5, self.text_height * 5))

        speed_x = self.width // 2 - 300
        self.base_canvas.draw_text(
            "SP:", (speed_x, self.height - self.speed_height * 0), size=2.5
        )
        self.base_canvas.draw_text(
            "REC:", (speed_x, self.height - self.speed_height * 1), size=2.5
        )
        self.base_canvas.draw_text(
            "MAX:", (speed_x, self.height - self.speed_height * 2), size=2.5
        )

    def _update_data_layer(self):
        self.data_canvas.clear()
        self.message_canvas.clear()

        if self.data["power"].get() != 0:
            self.draw_power_rec_power()

        if self.data["cadence"].get() != 0:
            self.draw_cadence()

        if self.data["reed_velocity"].get() != 0:
            self.draw_max_rec_reed_velocity()

        if self.data["reed_distance"].get() != 0:
            self.draw_distance()

        if self.data.has_message():
            self.draw_messages()

    def draw_power_rec_power(self):
        power = self.data["power"].get()
        rec_power = self.data["rec_power"].get()
        tolerance = 0.05

        # Display recommended power
        if self.data["rec_power"].is_valid():
            rec_power_text = "{0}".format(round(rec_power, 2))
        else:
            rec_power_text = "--"
        self.data_canvas.draw_text(rec_power_text, (340, self.text_height * 1))

        # Display power
        if self.data["power"].is_valid():
            power_text = "{0}".format(round(power, 2))
            if self.data["rec_power"].is_valid():
                if power > (rec_power + (rec_power * tolerance)):
                    power_colour = Colour.red
                elif power > rec_power:
                    power_colour = Colour.green
            else:
                power_colour = Colour.black
        else:
            power_text = "--"
            power_colour = Colour.black

        self.data_canvas.draw_text(
            power_text, (340, self.text_height * 2), colour=power_colour,
        )

    def draw_cadence(self):
        cadence = self.data["cadence"].get()
        if self.data["cadence"].is_valid():
            cadence_text = "{0}".format(round(cadence, 2))
        else:
            cadence_text = "--"
        self.data_canvas.draw_text(cadence_text, (340, self.text_height * 3))

    def draw_max_rec_reed_velocity(self):
        # Max Speed
        max_speed = self.data["predicted_max_speed"].get()
        if self.data["predicted_max_speed"].is_valid():
            max_speed_text = "{0} km/h".format(round(max_speed, 2))
        else:
            max_speed_text = "--"
        max_speed_pos = (
            self.width // 2 - 70,
            self.height - self.speed_height * 2,
        )
        self.data_canvas.draw_text(max_speed_text, max_speed_pos, size=2.5)

        # Recommended speed
        rec_speed = self.data["rec_speed"].get()
        if self.data["rec_speed"].is_valid():
            rec_speed_text = "{0} km/h".format(round(rec_speed, 2))
        else:
            rec_speed_text = "--"
        rec_speed_pos = (
            self.width // 2 - 70,
            self.height - self.speed_height * 1,
        )
        self.data_canvas.draw_text(rec_speed_text, rec_speed_pos, size=2.5)

        # Actual speed
        speed = self.data["reed_velocity"].get()
        speed_pos = (self.width // 2 - 70, self.height - self.speed_height * 0)
        tolerance = 0.05
        if self.data["reed_velocity"].is_valid():
            speed_text = "{0} km/h".format(round(speed, 2))
            if self.data["rec_speed"].is_valid():
                if speed > (rec_speed + (rec_speed * tolerance)):
                    speed_colour = Colour.red
                elif speed > rec_speed:
                    speed_colour = Colour.green
            else:
                speed_colour = Colour.black
        else:
            speed_text = "--"
            speed_colour = Colour.black
        self.data_canvas.draw_text(
            speed_text, speed_pos, colour=speed_colour, size=2.5
        )

    def draw_distance(self):
        reed_distance = self.data["reed_distance"].get()
        if self.data["reed_distance"].is_valid():
            reed_distance_text = "{0}".format(round(reed_distance, 2))
        else:
            reed_distance_text = "--"
        self.data_canvas.draw_text(
            reed_distance_text, (340, self.text_height * 4)
        )

    def draw_messages(self):
        message = self.data.get_message()
        self.message_canvas.draw_text(
            message, (340, self.text_height * 5), size=1.2, colour=Colour.red
        )


if __name__ == "__main__":
    args = Overlay.get_overlay_args(
        "Overlay displaying all (or just many) statistics"
    )
    my_overlay = OverlayAllStats(args.bike, args.bg)
    my_overlay.connect(ip=args.host)
