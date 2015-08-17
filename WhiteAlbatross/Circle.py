# encoding: utf8
import math

from PySide.QtCore import QPoint

from WhiteAlbatross.Figure import distance, Figure


# noinspection PyPep8Naming
class Circle(Figure):
    def __init__(self, x=0, y=0, radius=0):
        Figure.__init__(self)
        self.x = x
        self.y = y
        self.radius = radius
        self.rx = 0
        self.ry = 0

    def setPoint1(self, point):
        self.x = point.x()
        self.y = point.y()

    def setPoint2(self, point):
        self.rx = point.x()
        self.ry = point.y()
        self.radius = self.calcRadius(point)
        return True

    def calcRadius(self, point):
        return math.sqrt(math.pow(point.y() - self.y, 2) +
                         math.pow(point.x() - self.x, 2))

    def inSide(self, point):
        radius = self.calcRadius(point)
        return radius < self.radius

    def isControlPoint(self, point):
        dist1 = distance(QPoint(self.x, self.y), point)
        dist2 = distance(QPoint(self.rx, self.ry), point)
        return dist1 < Figure.CTRL or dist2 < Circle.CTRL

    def moveControlPoint(self, point):
        if self.mode is not Figure.MODE_CONTROL:
            return

        center = QPoint(self.x, self.y)
        dist1 = distance(center, point)
        delta = point - center

        radius = self.calcRadius(point)
        dist2 = distance(QPoint(self.rx, self.ry), point)

        if dist1 < dist2:
            self.x = point.x()
            self.y = point.y()
            self.rx += delta.x()
            self.ry += delta.y()
        else:
            self.radius = radius
            self.rx = point.x()
            self.ry = point.y()

    def draw(self, painter):
        painter.drawEllipse(QPoint(self.x, self.y), self.radius, self.radius)
        painter.drawEllipse(self.x - Circle.CTRL / 2, self.y - Circle.CTRL / 2, Circle.CTRL, Circle.CTRL)
        painter.drawEllipse(self.rx - Circle.CTRL / 2, self.ry - Circle.CTRL / 2, Circle.CTRL, Circle.CTRL)
        # painter.drawEllipse(self.x2, self.y2, 3, 3)

    def getDict(self):
        return {
            'circle': {
                'x': self.x,
                'y': self.y,
                'radius': self.radius
            }
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Circle(({x}, {y}), {radius})'.format(x=self.x, y=self.y, radius=self.radius)
