# encoding: utf8
from PySide.QtGui import QPolygon

from WhiteAlbatross.Point import Point
from WhiteAlbatross.Figure import Figure, distance
from WhiteAlbatross.State import State

# class


# noinspection PyPep8Naming
class Polygon(Figure):
    def __init__(self):
        Figure.__init__(self)
        self.points = []

        self.convex_polygons = []

    def draw(self, painter):
        painter.drawPolygon(QPolygon([p.qpoint() for p in self.points]))
        for point in self.points:
            point.draw(painter, Figure.CTRL)

    def getDict(self):
        return {'polygon': {'editor': [point.getDict() for point in self.points]}}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Polygon(' + ('{}' * len(self.points)).format(*self.points) + ')'
