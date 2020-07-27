from overlay import Overlay
from canvas import Colour

class OverlayBlank(Overlay):

	def __init__(self, bike=None, bg=None):
		super(OverlayBlank, self).__init__(bike, bg=bg)

	def on_connect(self, client, userdata, flags, rc):
		print('Connected with rc: {}'.format(rc))

		# To draw static text/whatever onto the overlay, draw on the base canvas
		self.base_canvas.draw_text("Blank overlay", (10, self.height - 10), 4, colour=Colour.white)

	def _update_data_layer(self):
		self.data_canvas.clear()

		# Content that changes each frame should be drawn to self.data_canvas here

if __name__ == '__main__':
	args = Overlay.get_overlay_args("An empty, example overlay")
	my_overlay = OverlayBlank(args.bike, args.bg)
	my_overlay.connect(ip=args.host)
