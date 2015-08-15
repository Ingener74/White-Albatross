# encoding: utf8
from PySide.QtCore import QPoint


class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def qpoint(self):
        return QPoint(self.x, self.y)

    def __repr__(self):
        return 'Point({x}, {y})'.format(x=self.x, y=self.y)

    def __str__(self):
        return self.__repr__()
