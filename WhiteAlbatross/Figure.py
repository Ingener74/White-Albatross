# encoding: utf8
import math

from PySide.QtCore import Qt
from PySide.QtGui import QColor, QPen, QBrush

from WhiteAlbatross.State import State


def distance(point1, point2):
    return math.sqrt(math.pow(point2.y() - point1.y(), 2) +
                     math.pow(point2.x() - point1.x(), 2))


class Delete(State):
    def __init__(self):
        State.__init__(self)


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
        self.delete = Delete()
        self.state = state

    def mouseDown(self, *args, **kwargs):
        return self.state.mouseDown(self, *args, **kwargs)

    def mouseMove(self, *args, **kwargs):
        self.state.mouseMove(self, *args, **kwargs)

    def mouseUp(self, *args, **kwargs):
        self.state.mouseUp(self, *args, **kwargs)

    def draw(self, painter, scale):
        self.state.draw(painter, scale)

    def getDict(self):
        raise NotImplementedError

    @staticmethod
    def pointIsControl(control_point, point, scale):
        # return distance(control_point, point) < Figure.CTRL_RADIUS / scale
        return distance(control_point, point) < Figure.CTRL_RADIUS

    def lineWidth(self, scale):
        return 2

    def drawControlPoint(self, painter, point, color, scale):
        painter.setPen(QPen(QBrush(color), self.lineWidth(scale), Qt.SolidLine))
        # painter.drawEllipse(point, Figure.CTRL_RADIUS / scale, Figure.CTRL_RADIUS / scale)
        painter.drawEllipse(point, Figure.CTRL_RADIUS, Figure.CTRL_RADIUS)
