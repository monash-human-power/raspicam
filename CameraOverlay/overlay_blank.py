from overlay import Overlay, Color

class OverlayBlank(Overlay):

	def __init__(self):
		super(OverlayBlank, self).__init__()

	def on_connect(self, client, userdata, flags, rc):
		print('Connected with rc: {}'.format(rc))

		self.draw_text(self.base_overlay, "Blank overlay", (10, self.height - 10), 4, color=Color.white)

	def on_message(self, client, userdata, msg):
		topic = msg.topic
		print(topic + " " + str(msg.payload.decode("utf-8")))


if __name__ == '__main__':
	my_overlay = OverlayBlank()
	my_overlay.connect(ip="localhost")
