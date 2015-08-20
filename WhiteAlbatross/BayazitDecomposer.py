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

    def decompose(self, poly):

        # for i, p1 in enumerate(poly):
        #     if  is_reflex(poly, p1):
        #         self.reflex_vertices.append(p1)
        #         upperDist = lowerDist = sys.maxint
        #         for j, p2 in enumerate(poly):
        #             if left(poly[i - 1], p1, p2) and right_on(poly[i - 1], p1, poly[j - 1]):
        #                 p = intersection(poly[i - 1], p1, p2, poly[j - 1])
        #                 if right(poly[(i + 1) if len(poly) > (i + 1) else 0], p1, p):
        #                     d = sqdist(poly[i], p)
        #                     if d < lowerDist:
        #                         lowerDist = d
        #                         lowerInt = p
        #                         lowerIndex = j
        #             if left(at(poly, i + 1), at(poly, i), at(poly, j + 1)) and right_on(at(poly, i + 1), at(poly, i), at(poly, j)):
        #                 p = intersection(at(poly, i + 1), at(poly, i), at(poly, j), at(poly, j + 1));
        #                 if left(at(poly, i - 1), at(poly, i), p):
        #                     d = sqdist(poly[i], p);
        #                     if d < upperDist:
        #                         upperDist = d;
        #                         upperInt = p;
        #                         upperIndex = j;

        #         // if there are no vertices to connect to, choose a point in the middle
        #         if (lowerIndex == (upperIndex + 1) % poly.size()) {
        #             printf("Case 1: Vertex(%d), lowerIndex(%d), upperIndex(%d), poly.size(%d)\n", i, lowerIndex, upperIndex, (int) poly.size());
        #             p.x = (lowerInt.x + upperInt.x) / 2;
        #             p.y = (lowerInt.y + upperInt.y) / 2;
        #             steinerPoints.push_back(p);
        #
        #             if (i < upperIndex) {
        #                 lowerPoly.insert(lowerPoly.end(), poly.begin() + i, poly.begin() + upperIndex + 1);
        #                 lowerPoly.push_back(p);
        #                 upperPoly.push_back(p);
        #                 if (lowerIndex != 0) upperPoly.insert(upperPoly.end(), poly.begin() + lowerIndex, poly.end());
        #                 upperPoly.insert(upperPoly.end(), poly.begin(), poly.begin() + i + 1);
        #             } else {
        #                 if (i != 0) lowerPoly.insert(lowerPoly.end(), poly.begin() + i, poly.end());
        #                 lowerPoly.insert(lowerPoly.end(), poly.begin(), poly.begin() + upperIndex + 1);
        #                 lowerPoly.push_back(p);
        #                 upperPoly.push_back(p);
        #                 upperPoly.insert(upperPoly.end(), poly.begin() + lowerIndex, poly.begin() + i + 1);
        #             }
        #         } else {
        #             // connect to the closest point within the triangle
        #             printf("Case 2: Vertex(%d), closestIndex(%d), poly.size(%d)\n", i, closestIndex, (int) poly.size());
        #
        #             if (lowerIndex > upperIndex) {
        #                 upperIndex += poly.size();
        #             }
        #             closestDist = numeric_limits<Scalar>::max();
        #             for (int j = lowerIndex; j <= upperIndex; ++j) {
        #                 if (leftOn(at(poly, i - 1), at(poly, i), at(poly, j))
        #                         && rightOn(at(poly, i + 1), at(poly, i), at(poly, j))) {
        #                     d = sqdist(at(poly, i), at(poly, j));
        #                     if (d < closestDist) {
        #                         closestDist = d;
        #                         closestVert = at(poly, j);
        #                         closestIndex = j % poly.size();
        #                     }
        #                 }
        #             }
        #
        #             if (i < closestIndex) {
        #                 lowerPoly.insert(lowerPoly.end(), poly.begin() + i, poly.begin() + closestIndex + 1);
        #                 if (closestIndex != 0) upperPoly.insert(upperPoly.end(), poly.begin() + closestIndex, poly.end());
        #                 upperPoly.insert(upperPoly.end(), poly.begin(), poly.begin() + i + 1);
        #             } else {
        #                 if (i != 0) lowerPoly.insert(lowerPoly.end(), poly.begin() + i, poly.end());
        #                 lowerPoly.insert(lowerPoly.end(), poly.begin(), poly.begin() + closestIndex + 1);
        #                 upperPoly.insert(upperPoly.end(), poly.begin() + closestIndex, poly.begin() + i + 1);
        #             }
        #         }
        #
        #         // solve smallest poly first
        #         if (lowerPoly.size() < upperPoly.size()) {
        #             decomposePoly(lowerPoly);
        #             decomposePoly(upperPoly);
        #         } else {
        #             decomposePoly(upperPoly);
        #             decomposePoly(lowerPoly);
        #         }
        #         return;
        #     }
        # }
        # polys.push_back(poly);

        return [[point for point in polygon]]
