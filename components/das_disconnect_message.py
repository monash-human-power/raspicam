from components.message import Message
from canvas import Canvas, Colour
from data import Data


class DASDisconnectMessage(Message):
    """Class displays error message on overlay when DAS is not connected, or
    overlay is not connected to an MQTT broker.

    Attributes:
        text_colour: Colour type representing the colour of the message
        message: String representing the error message that displays on the
        overlay
        client: MQTT Client which is used to check if client is connected
    """

    # These class variables must be consistent for every instance
    text_colour = Colour.red
    message = "Message: DAS is disconnected, ensure it is turned on."

    def __init__(self, client):
        """Assign client as an instance variable to check whether client used
        for the overlay is connected."""
        self.client = client

    def draw_data(self, canvas: Canvas, data: Data) -> None:
        if not self.client.is_connected():
            self._display_message(
                canvas,
                DASDisconnectMessage.message,
                DASDisconnectMessage.text_colour,
            )
