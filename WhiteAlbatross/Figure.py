# encoding: utf8
from abc import abstractmethod
import math


def distance(point1, point2):
    return math.sqrt(math.pow(point2.y() - point1.y(), 2) +
                     math.pow(point2.x() - point1.x(), 2))


# noinspection PyPep8Naming
class Figure(object):
    CTRL = 7

    def __init__(self):
        pass

    @abstractmethod
    def setPoint1(self, point):
        raise NotImplementedError

    @abstractmethod
    def setPoint2(self, point):
        raise NotImplementedError

    @abstractmethod
    def inSide(self, point):
        raise NotImplementedError

    @abstractmethod
    def isControlPoint(self, point):
        raise NotImplementedError

    @abstractmethod
    def draw(self, painter):
        raise NotImplementedError
