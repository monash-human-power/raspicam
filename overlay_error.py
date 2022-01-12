from overlay_new import OverlayNew

DEFAULT_TEST_BIKE = "v3"


class OverlayErrorTest(OverlayNew):
    """
    Overlay made for testing MQTT error publishing by inheriting OverlayNew

    Tests whether an error will be published onto the MQTT Camera Errors topic
    "/v3/camera/errors". This overlay should not be used for any purpose other
    than error testing. This script should not be triggered by Pytest.

    To exit the script, press CTRL+C.
    """

    def __init__(self, bike=DEFAULT_TEST_BIKE, bg=None, mqtt_username=None):
        super().__init__(bike, bg, mqtt_username=mqtt_username)

    def on_connect(self, client, userdata, flags, rc):
        """ Raises an exception which should be caught by _on_connect. """
        # Forcing an exception to occur
        raise Exception("Test error")


if __name__ == "__main__":
    args = OverlayErrorTest.get_overlay_args("Test Overlay")
    my_overlay = OverlayErrorTest(args.bike, args.bg, args.username)
    my_overlay.connect(ip=args.host)
