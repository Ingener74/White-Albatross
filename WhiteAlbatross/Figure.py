# encoding: utf8
import math
from PySide.QtGui import QColor


def distance(point1, point2):
    return math.sqrt(math.pow(point2.y() - point1.y(), 2) +
                     math.pow(point2.x() - point1.x(), 2))


# noinspection PyPep8Naming
class Figure(object):
    CTRL_RADIUS = 7

    COLORS = [
        QColor(0, 0, 0),
        QColor(255, 255, 255),
        QColor(255, 0, 0),
        QColor(0, 255, 0),
        QColor(0, 0, 255),
        QColor(255, 255, 0),
        QColor(0, 255, 255),
        QColor(255, 0, 255),
        QColor(192, 192, 192),
        QColor(128, 128, 128),
        QColor(128, 0, 0),
        QColor(128, 128, 0),
        QColor(0, 128, 0),
        QColor(128, 0, 128),
        QColor(0, 128, 128),
        QColor(0, 0, 128)
    ]

    def __init__(self, state):
        self.state = state

    def mouseDown(self, point):
        return self.state.mouseDown(point, self)

    def mouseMove(self, point):
        self.state.mouseMove(point, self)

    def mouseUp(self, point):
        self.state.mouseUp(point, self)

    def draw(self, painter):
        self.state.draw(painter)

    def getDict(self):
        raise NotImplementedError
