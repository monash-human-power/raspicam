from abc import ABC, abstractmethod

from canvas import Canvas
from data import Data

class Drawable(ABC):
    @abstractmethod
    def draw_base(self, canvas: Canvas):
        pass
    @abstractmethod
    def draw_data(self, canvas: Canvas, data: Data):
        pass
