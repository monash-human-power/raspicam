from components import Message
from canvas import Canvas, Colour
from data import Data


class DASDisconnectMessage(Message):
    """Class will display an error message on the overlay that the DAS is not
    connected.

    Only displays when DAS is disconnected. Disappears immediately as soon
    as it is connected.

    Attributes:
        text_colour: Colour type representing the colour of the message
        message: String representing the error message that displays on the
        overlay
        client: MQTT Client which is used to check if client is connected
    """

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
