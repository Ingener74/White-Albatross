# encoding: utf8
from PySide.QtGui import QPolygon

from WhiteAlbatross.Figure import Figure, distance
from WhiteAlbatross.State import State
from WhiteAlbatross.BayazitDecomposer import BayazitDecomposer


def qpoint2dict(point):
    return {'x': point.x(), 'y': point.y()}


def qpoint2str(point):
    return '({x}, {y})'.format(x=point.x(), y=point.y())


class AddPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, event, machine):
        for p in machine.points:
            if distance(p, event.pos()) < Figure.CTRL_RADIUS and p is not machine.points[0]:
                return True
        if len(machine.points) > 2 and distance(machine.points[0], event.pos()) < Figure.CTRL_RADIUS:
            machine.points.append(machine.points[0])

            # Decompose
            machine.convex_polygons = machine.decomposer.decompose(machine.points)

            machine.state = machine.control
        else:
            machine.points.append(event.pos())
        return True

    def mouseMove(self, point, machine):
        pass

    def mouseUp(self, point, machine):
        pass


class Control(State):
    def __init__(self):
        State.__init__(self)

        self.control1 = None

    def mouseDown(self, event, machine):
        for p in machine.points:
            if distance(p, event.pos()) < Figure.CTRL_RADIUS:
                self.control1 = p
                return True
        return False

    def mouseMove(self, event, machine):
        if self.control1:
            self.control1.setX(event.pos().x())
            self.control1.setY(event.pos().y())

    def mouseUp(self, event, machine):
        # Decompose
        machine.convex_polygons = machine.decomposer.decompose(machine.points)

        self.control1 = None


# noinspection PyPep8Naming
class Polygon(Figure):
    def __init__(self):

        self.add_point = AddPoint()
        self.control = Control()

        Figure.__init__(self, self.add_point)

        self.decomposer = BayazitDecomposer()

        self.points = []

        self.convex_polygons = []

    def draw(self, painter):
        painter.drawPolygon(QPolygon(self.points))

        for poly in self.convex_polygons:
            painter.drawPolygon(QPolygon(poly))

        for point in self.points:
            painter.drawEllipse(point, Figure.CTRL_RADIUS, Figure.CTRL_RADIUS)

    def getDict(self):
        return {'polygon': {'editor': [qpoint2dict(point) for point in self.points],
                            'convex': [qpoint2dict(point) for convex in self.convex_polygons for point in convex]}}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Polygon(' + ('{}' * len(self.points)).format(*[qpoint2str(point) for point in self.points]) + ')'
