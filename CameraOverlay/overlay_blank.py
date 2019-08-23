import numpy as np
import cv2
from overlay import Overlay


class OverlayBlank(Overlay):

	def __init__(self):
		super(OverlayBlank, self).__init__()

	def on_connect(self, client, userdata, flags, rc):
		print('Connected with rc: {}'.format(rc))

		self.overlay = np.zeros((self.height, self.width, 3), np.uint8)
		font = cv2.FONT_HERSHEY_PLAIN
		cv2.putText(self.overlay, 'Blank overlay', (10, self.height - 10), font, 4, (255, 255, 255), 2, cv2.LINE_AA)

	def on_message(self, client, userdata, msg):
		topic = msg.topic
		print(topic + " " + str(msg.payload.decode("utf-8")))


if __name__ == '__main__':
	my_overlay = OverlayBlank()
	my_overlay.connect(ip="localhost")
