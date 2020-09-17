from components.message import Message
from canvas import Colour

class DASDisconnectMessage(Message):
    text_colour = Colour.red

    def draw_data(self, canvas: Canvas, data: Data):
        disconnected_message = "Message: DAS is disconnected. Connect to a broker."
        self.display_message(canvas, disconnected_message, text_colour)