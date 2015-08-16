# encoding: utf8
from PySide.QtGui import QPolygon


class Polygon(object):
    def __init__(self):
        self.points = []

    def setPoint1(self, point):
        pass

    def setPoint2(self, point):
        return True

    def draw(self, painter):
        painter.drawPolygon(QPolygon([p.qpoint() for p in self.points]))

    def inSide(self, point):
        return False

    def isControlPoint(self, point):
        pass

    def moveControlPoint(self, point):
        pass

    def getDict(self):
        return {
            'polygon': {
            }
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Polygon()'
