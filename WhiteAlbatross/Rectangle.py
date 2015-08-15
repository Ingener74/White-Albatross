# encoding: utf8
from PySide.QtCore import QRect, QPoint


class Rectangle(object):
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def setPoint1(self, point):
        self.x1 = point.x()
        self.y1 = point.y()

    def setPoint2(self, point):
        self.x2 = point.x()
        self.y2 = point.y()

    def draw(self, painter):
        painter.drawRect(QRect(QPoint(self.x1, self.y1), QPoint(self.x2, self.y2)))