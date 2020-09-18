from components.message import Message
from canvas import Canvas, Colour
from data import Data


class DASDisconnectMessage(Message):
    """Class displays error message on overlay when DAS is not
    connected, or overlay is not connected to an MQTT broker.

    Attributes:
        text_colour: Colour type representing the colour of the message
    """

    text_colour = Colour.red
    message = "Message: DAS is disconnected. Connect to a broker."

    def draw_data(self, canvas: Canvas, data: Data):
        """Set up the disconnected message and pass it into the
        display_message method.

        Display message only whenever DAS is disconnected or overlay is not
        connected to broker.
        """
        self.display_message(
            canvas, DASDisconnectMessage.message, DASDisconnectMessage.text_colour
        )
