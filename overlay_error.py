"""
Tests whether an error will be published onto the MQTT Camera Errors topic
'/v3/camera/errors'

This overlay should not be used for any purpose other than testing. This script should
not be triggered by Pytest.
"""
from overlay_new import OverlayNew, Overlay
from camera_error_handler import CameraException

DEFAULT_TEST_BIKE = "v3"

class TestOverlay(OverlayNew):
    """
    Overlay made for testing MQTT error publishing by using OverlayNew's MQTT client
    
    To exit the script, press CTRL+C.
    """

    def __init__(self, bike=DEFAULT_TEST_BIKE, bg=None):
        super().__init__(bike, bg)
    
    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)

        # Forcing an exception to occur
        with CameraException(self.client, self.backend_name):
            raise Exception("Test error")

if __name__ == '__main__':
    args = Overlay.get_overlay_args("Test Overlay")
    my_overlay = TestOverlay(args.bike, args.bg)
    my_overlay.connect(ip=args.host)
    