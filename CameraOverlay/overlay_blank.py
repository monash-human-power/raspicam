from overlay import Overlay, Colour

class OverlayBlank(Overlay):

	def __init__(self):
		super(OverlayBlank, self).__init__()

	def on_connect(self, client, userdata, flags, rc):
		print('Connected with rc: {}'.format(rc))

		# To draw static text/whatever onto the overlay, draw on the base canvas
		self.base_canvas.draw_text("Blank overlay", (10, self.height - 10), 4, colour=Colour.white)

	def update_data_layer(self):
		self.data_canvas.clear()

		# Content that changes each frame should be drawn to self.data_canvas here

if __name__ == '__main__':
	args = Overlay.get_overlay_args("An empty, example overlay")
	my_overlay = OverlayBlank()
	my_overlay.connect(ip="192.168.1.154")
