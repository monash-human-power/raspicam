import cv2
from enum import Enum
import numpy as np

class Colour(Enum):
	# Remember, OpenCV uses BGR(A) not RGB(A)
	white = (255, 255, 255, 255)
	black = (0, 0, 0, 255)
	transparentBlack = (0, 0, 0, 0)
	blue = (255, 0, 0, 255)
	green = (0, 255, 0, 255)
	red = (0, 0, 255, 255)

class Canvas():
	""" A writeable image, for creating overlay content """

	def __init__(self, width, height):
		""" Initialises to plain black and transparent """
		self.width = width
		self.height = height
		self.img = None
		self.clear()

	def clear(self):
		""" Sets the entire canvas contents to transparent black """
		self.img = np.zeros((self.height, self.width, 4), np.uint8)

	@staticmethod
	def _get_colour_tuple(colour):
		""" Internal method - takes a 3-tulpe, 4-tuple or Colour class and returns a 4-tuple colour """
		if isinstance(colour, Colour):
			return colour.value
		if len(colour) == 3:
			return colour + (255,)
		return colour

	def draw_text(self, text, coord, size=1.5, colour=Colour.black):
		""" Draws text to the canvas.

		    The bottom left corner of the text is given by the tuple coord.
		    (the top left of the screen is the origin) """
		colour = Canvas._get_colour_tuple(colour)
		font = cv2.FONT_HERSHEY_SIMPLEX
		# By default thickness = size if thickness isn't specified,
		# but it's a little thin especially on a small screen
		thickness_increase = 0.5
		thickness = round(size + thickness_increase)
		cv2.putText(self.img, text, coord, font, size, colour, thickness, cv2.LINE_AA)

	def draw_rect(self, top_left, bottom_right, colour=Colour.black):
		""" Draws a rectangle to the canvas.

		    top_left and bottom_right are tuples, and specify the dimensions of the rectangle
		    (the top left of the screen is the origin) """
		colour = Canvas._get_colour_tuple(colour)
		cv2.rectangle(self.img, top_left, bottom_right, colour, thickness=cv2.FILLED)

	def copy_to(self, dest):
		""" Writes the contents of self.img over dest, accounting for transparency.

		    Use this method to put the overlay contents over the video feed """
		# Extract the alpha mask of the BGRA canvas, convert to BGR
		blue, green, red, alpha = cv2.split(self.img)
		minimum_alpha = 180 # alpha must be > this value to show a pixel
		img = cv2.merge((blue, green, red))
		_, mask = cv2.threshold(alpha, minimum_alpha, 255, cv2.THRESH_BINARY)

		# Black-out the area behind the canvas on the destination
		dest = cv2.bitwise_and(dest, dest, mask=cv2.bitwise_not(mask))
		return cv2.add(dest, img)