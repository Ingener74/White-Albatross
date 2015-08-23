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

        self.polys = []

    def __make_ccw(self, poly):
        br = 0

        for i, p in enumerate(poly):
            if p.x() < poly[br].y() or (p.y() == poly[br].y() and p.x() > poly[br].x()):
                br = i

        if not left(poly[br - 1], poly[br], poly[(br + 1) if len(poly) > (br + 1) else 0]):
            # print u'Переверул ломаную по часовой стрелке'
            return poly[::-1]
        # print u'Ломаная по часовой стрелке'
        return poly[:]

    def __decompose(self, poly):
        lower_poly = []
        upper_poly = []

        upper_int = QPoint(0, 0)
        lower_int = QPoint(0, 0)

        upper_index = 0
        lower_index = 0
        closest_index = 0

        p = QPoint(0, 0)

        for pi in poly:
            if is_reflex(poly, pi):

                pim1 = poly[-1 if pi is poly[0] else poly.index(pi) - 1]
                pip1 = poly[0 if pi is poly[-1] else poly.index(pi) + 1]

                self.reflex_vertices.append(pi)
                upper_dist = sys.maxint
                lower_dist = sys.maxint

                for pj in poly:
                    pjm1 = poly[-1 if pj is poly[0] else poly.index(pj) - 1]
                    pjp1 = poly[0 if pj is poly[-1] else poly.index(pj) + 1]

                    if left(pim1, pi, pj) and right_on(pim1, pi, pjm1):
                        p = intersection(pim1, pi, pj, pjm1)
                        if right(pip1, pi, p):
                            d = sqdist(pi, p)
                            if d < lower_dist:
                                lower_dist = d
                                lower_int = p
                                lower_index = poly.index(pj)

                    if left(pip1, pi, pjp1) and right_on(pip1, pi, pj):
                        p = intersection(pip1, pi, pj, pjp1)
                        if left(pim1, pi, p):
                            d = sqdist(pi, p)
                            if d < upper_dist:
                                upper_dist = d
                                upper_int = p
                                upper_index = poly.index(pj)

                i = poly.index(pi)
                if lower_index == ((upper_index + 1) % len(poly)):
                    p.setX((lower_int.x() + upper_int.x()) / 2)
                    p.setY((lower_int.y() + upper_int.y()) / 2)

                    self.steiner_points.append(p)

                    if i < upper_index:
                        lower_poly += poly[i:upper_index + 1]

                        lower_poly.append(p)
                        upper_poly.append(p)
                        if lower_index != 0:
                            upper_poly += poly[lower_index:]

                        upper_poly += poly[:i + 1]
                    else:
                        if i != 0:
                            lower_poly += poly[i:]

                        lower_poly += poly[:upper_index + 1]
                        lower_poly.append(p)
                        upper_poly.append(p)

                        upper_poly += poly[lower_index:i+1]
                else:
                    if lower_index > upper_index:
                        upper_index += len(poly)

                    closest_dist = sys.float_info.max
                    for j in xrange(lower_index, upper_index + 1):

                        pj = poly[j % len(poly)]

                        if left_on(pim1, pi, pj) and right_on(pip1, pi, pj):
                            d = sqdist(pi, pj)
                            if d < closest_dist:
                                closest_dist = d
                                closest_index = j % len(poly)

                    if i < closest_index:
                        lower_poly += poly[i:closest_index + 1]
                        if closest_index != 0:
                            upper_poly += poly[closest_index:]

                        upper_poly += poly[:i + 1]
                    else:
                        if i != 0:
                            lower_poly += poly[i:]

                        lower_poly += poly[:closest_index + 1]
                        upper_poly += poly[closest_index:i + 1]

                if len(lower_poly) < len(upper_poly):
                    self.decompose(lower_poly)
                    self.decompose(upper_poly)
                else:
                    self.decompose(upper_poly)
                    self.decompose(lower_poly)
                return

        self.polys.append(poly)

    def decompose(self, poly):
        self.__decompose(self.__make_ccw(poly))
        return self.polys

