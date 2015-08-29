# encoding: utf8
from PySide.QtCore import QPoint


def qpoint2dict(point):
    return {'x': point.x(), 'y': point.y()}


def dict2qpoint(dictionary):
    return QPoint(dictionary['x'], dictionary['y'])


def qpoint2str(point):
    return '({x}, {y})'.format(x=point.x(), y=point.y())