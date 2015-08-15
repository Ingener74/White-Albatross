# encoding: utf8
from PySide.QtGui import QPolygon


class Polygon(object):
    def __init__(self):
        self.points = []

    def setPoint1(self, point):
        pass

    def setPoint2(self, point):
        pass

    def draw(self, painter):
        painter.drawPolygon(QPolygon([p.qpoint() for p in self.points]))