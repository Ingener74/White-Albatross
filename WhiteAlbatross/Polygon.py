# encoding: utf8
from PySide.QtGui import QPolygon

from WhiteAlbatross.Figure import Figure, distance
from WhiteAlbatross.State import State


def qpoint2dict(point):
    return {'x': point.x(), 'y': point.y()}


def qpoint2str(point):
    return '({x}, {y})'.format(x=point.x(), y=point.y())


class AddPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, point, machine):
        for p in machine.points:
            if distance(p, point) < Figure.CTRL and p is not machine.points[0]:
                return True
        if len(machine.points) > 2 and distance(machine.points[0], point) < Figure.CTRL:
            machine.points.append(machine.points[0])
            machine.state = machine.control
        else:
            machine.points.append(point)
        return True

    def mouseMove(self, point, machine):
        pass

    def mouseUp(self, point, machine):
        pass


class Control(State):
    def __init__(self):
        State.__init__(self)

        self.control1 = None

    def mouseDown(self, point, machine):
        for p in machine.points:
            if distance(p, point) < Figure.CTRL:
                self.control1 = p
                return True
        return False

    def mouseMove(self, point, machine):
        if self.control1:
            self.control1.setX(point.x())
            self.control1.setY(point.y())

    def mouseUp(self, point, machine):
        self.control1 = None


# noinspection PyPep8Naming
class Polygon(Figure):
    def __init__(self):

        self.add_point = AddPoint()
        self.control = Control()

        Figure.__init__(self, self.add_point)
        self.points = []

        self.convex_polygons = []

    def draw(self, painter):
        painter.drawPolygon(QPolygon(self.points))
        for point in self.points:
            painter.drawEllipse(point, Figure.CTRL, Figure.CTRL)

    def getDict(self):
        return {'polygon': {'editor': [qpoint2dict(point) for point in self.points]}}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Polygon(' + ('{}' * len(self.points)).format(*[qpoint2str(point) for point in self.points]) + ')'
