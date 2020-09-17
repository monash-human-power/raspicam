from components.message import Message
from canvas import Canvas, Colour


class DASDisconnectMessage(Message):
    """Class displays error message on overlay when DAS is not
    connected, or overlay is not connected to an MQTT broker.

    Extends the Message class.

    Attributes:
        text_colour: Colour type representing the colour of the message
    """

    text_colour = Colour.red

    def draw_data(self, canvas: Canvas):
        """Set up the disconnected message and pass it into the
        display_message method.

        Display message only whenever DAS is disconnected or overlay is not
        connected to broker.
        """
        disconnected_message = (
            "Message: DAS is disconnected. Connect to a broker."
        )
        self.display_message(
            canvas, disconnected_message, DASDisconnectMessage.text_colour
        )
