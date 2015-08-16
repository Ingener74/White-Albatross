# encoding: utf8
import math

from PySide.QtCore import QPoint

from WhiteAlbatross.Figure import distance


# noinspection PyPep8Naming
class Circle(object):
    CTRL = 9

    def __init__(self, x=0, y=0, radius=0):
        self.x = x
        self.y = y
        self.radius = radius

    def setPoint1(self, point):
        self.x = point.x()
        self.y = point.y()

    def setPoint2(self, point):
        self.radius = self.calcRadius(point)

    def calcRadius(self, point):
        return math.sqrt(math.pow(point.y() - self.y, 2) +
                         math.pow(point.x() - self.x, 2))

    def inSide(self, point):
        radius = self.calcRadius(point)
        return radius < self.radius

    def isControlPoint(self, point):
        radius = self.calcRadius(point)

        dist = distance(QPoint(self.x, self.y), point)
        return math.fabs(self.radius - radius) < Circle.CTRL / 2 or dist < Circle.CTRL / 2

    def moveControlPoint(self, point):
        dist = distance(QPoint(self.x, self.y), point)
        if dist < Circle.CTRL / 2:
            self.x = point.x()
            self.y = point.y()

        radius = self.calcRadius(point)
        if math.fabs(self.radius - radius) < Circle.CTRL:
            self.radius = radius

    def draw(self, painter):
        painter.drawEllipse(QPoint(self.x, self.y), self.radius, self.radius)
        painter.drawEllipse(self.x - Circle.CTRL / 2, self.y - Circle.CTRL / 2, Circle.CTRL, Circle.CTRL)
        # painter.drawEllipse(self.x2, self.y2, 3, 3)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Circle(({x}, {y}), {radius})'.format(x=self.x, y=self.y, radius=self.radius)
