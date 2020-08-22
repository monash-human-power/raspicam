from abc import ABC, abstractmethod

from canvas import Canvas
from data import Data


class Component(ABC):
    @abstractmethod
    def draw_base(self, canvas: Canvas):
        """ Called a single time in order to draw the static, unchanging parts
            of this overlay component. """

    @abstractmethod
    def draw_data(self, canvas: Canvas, data: Data):
        """ Called at a regular interval to update dynamic data being displayed
            on the overlay from this component. """
