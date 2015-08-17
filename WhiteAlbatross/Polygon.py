# encoding: utf8
from PySide.QtGui import QPolygon

from WhiteAlbatross.Point import Point
from WhiteAlbatross.Figure import Figure, distance


# noinspection PyPep8Naming
class Polygon(Figure):
    def __init__(self):
        Figure.__init__(self)
        self.points = []

        self.convex_polygons = []

    def setPoint1(self, point):
        self.points.append(Point(point.x(), point.y()))

    def setPoint2(self, point):

        if len(self.points) < 2:
            self.setPoint1(point)
            return False

        first_point = self.points[0]
        last_point = self.points[len(self.points) - 1]
        if distance(first_point.qpoint(), point) < Figure.CTRL:
            last_point.x = first_point.x
            last_point.y = first_point.y
            return True
        else:
            last_point.x = point.x()
            last_point.y = point.y()
            return False

    def draw(self, painter):
        painter.drawPolygon(QPolygon([p.qpoint() for p in self.points]))
        for point in self.points:
            point.draw(painter, Figure.CTRL)

    def inSide(self, point):
        return False

    def isControlPoint(self, point):
        pass

    def moveControlPoint(self, point):
        pass

    def getDict(self):
        return {'polygon': {'editor': [point.getDict() for point in self.points]}}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Polygon(' + ('{}' * len(self.points)).format(*self.points) + ')'
