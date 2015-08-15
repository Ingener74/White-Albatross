# encoding: utf8
from PySide.QtCore import QPoint
import math


class Circle(object):
    def __init__(self, x=0, y=0, radius=0):
        self.x = x
        self.y = y
        self.radius = radius

    def setPoint1(self, point):
        self.x = point.x()
        self.y = point.y()

    def setPoint2(self, point):
        self.radius = math.sqrt(math.pow(point.y() - self.y, 2) +
                                math.pow(point.x() - self.x, 2))

    def draw(self, painter):
        painter.drawEllipse(QPoint(self.x, self.y), self.radius, self.radius)
