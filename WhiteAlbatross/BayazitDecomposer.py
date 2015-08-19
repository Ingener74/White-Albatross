# encoding: utf8
import math
import sys


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


def is_reflex(poly, point):
    i = poly.index(point)
    a = poly[i - 1]
    b = poly[i]
    c = poly[(i + 1) if len(poly) > (i + 1) else 0]
    return right(a, b, c)

class BayazitDecomposer(object):
    """
    http://mpen.ca/406/bayazit
    """
    def __init__(self):
        self.reflex_vertices = []
        self.steiner_points = []

    def decompose(self, polygon):



        for point in polygon:
            if is_reflex(polygon, point):
                self.reflex_vertices.append(point)

                upperDist = lowerDist = sys.maxint


        return [[point for point in polygon]]
