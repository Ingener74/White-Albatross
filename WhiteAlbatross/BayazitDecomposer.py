# encoding: utf8
import math
import sys
from PySide.QtCore import QPoint


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
    return math.fabs(a - b) <= 1e-8


def wrap(a, b):
    pass


def srand(min, max):
    pass


def intersection(p1, p2, q1, q2):
    a1 = p2.y() - p1.y()
    b1 = p1.x() - p2.x()
    c1 = a1 * p1.x() + b1 * p1.y()
    a2 = q2.y() - q1.y()
    b2 = q1.x() - q2.x()
    c2 = a2 * q1.x() + b2 * q1.y()
    det = a1 * b2 - a2*b1
    if not eq(det, 0):
        return QPoint((b2 * c1 - b1 * c2) / det, (a1 * c2 - a2 * c1) / det)
    else:
        return QPoint()


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
        # for i, point in enumerate(polygon):
        #     if is_reflex(polygon, point):
        #         self.reflex_vertices.append(point)
        #
        #         upper_dist = lower_dist = sys.maxint
        #
        #         for j, p2 in enumerate(polygon):
        #             if left(polygon[i-1], point, polygon[j]) and right_on(polygon[i-1], point, polygon[j-1]):
        #                 inter_point =

        return [[point for point in polygon]]
