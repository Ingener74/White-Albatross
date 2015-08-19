# encoding: utf8
import math


def area(a, b, c):
    return (b.x() - a.x())*(c.y() - a.y()) - ((c.x() - a.x())*(b.y() - a.y()))


def left(a, b, c):
    return area(a, b, c) > 0


def left_on(a, b, c):
    return area(a, b, c) >= 0


def right(a, b, c):
    return area(a, b, c) < 0


def right_on(a, b, c):
    return area(a, b, c) <= 0


def collinear(a, b, c):
    return area(a, b, c) == 0


def sqdist(a, b):
    return math.pow(b.x() - a.x(), 2) + math.pow(b.y() - a.y(), 2)


def eq(a, b):
    pass


def wrap(a, b):
    pass


def srand(min, max):
    pass


class BayazitDecomposer(object):
    """
    http://mpen.ca/406/bayazit
    """
    def __init__(self):
        pass

    def decompose(self, polygon):



        return [[point for point in polygon]]
