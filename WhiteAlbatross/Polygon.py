# encoding: utf8
from PySide.QtCore import Qt, QPoint
from PySide.QtGui import QPolygon, QPen, QColor, QBrush

from WhiteAlbatross.Figure import Figure, distance
from WhiteAlbatross.State import State
from WhiteAlbatross.BayazitDecomposer import BayazitDecomposer


def qpoint2dict(point):
    return {'x': point.x(), 'y': point.y()}


def dict2qpoint(dictionary):
    return QPoint(dictionary['x'], dictionary['y'])


def qpoint2str(point):
    return '({x}, {y})'.format(x=point.x(), y=point.y())


class AddPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, point, machine):
        # Если нажатие в какой нибудь точке кроме последней то просто ничего не делаем и выходим
        for p in machine.points:
            if distance(p, point) < Figure.CTRL_RADIUS and p is not machine.points[-1]:
                return True  # новую фигуру добавлять не надо

        # Если у нас больше 1 точки и мы тыкаем в последнюю тогда ...
        if len(machine.points) > 1 and distance(machine.points[-1], point) < Figure.CTRL_RADIUS:
            # ... делаем декомпозицию ломаной и ...
            machine.decompose()

            # ... и переходим в состояние управление ломаной
            machine.state = machine.control
            return True

        # в любом оставшемся случае добавляем точку в ломаную
        machine.points.append(point)
        return True  # новую фигуру добавлять не надо


class Control(State):
    def __init__(self):
        State.__init__(self)

        self.control1 = None

    def mouseDown(self, point, machine):
        for p in machine.points:
            if distance(p, point) < Figure.CTRL_RADIUS:
                self.control1 = p
                return True
        return False

    def mouseMove(self, point, machine):
        if self.control1:
            self.control1.setX(point.x())
            self.control1.setY(point.y())

    def mouseUp(self, point, machine):
        if self.control1:
            # Разбиение
            machine.decompose()

        self.control1 = None

    def draw(self, painter):
        if self.control1:
            painter.drawEllipse(self.control1, Figure.CTRL_RADIUS + 4, Figure.CTRL_RADIUS + 4)


# noinspection PyPep8Naming
class Polygon(Figure):
    def __init__(self):

        self.add_point = AddPoint()
        self.control = Control()

        Figure.__init__(self, self.add_point)

        self.decomposer = BayazitDecomposer()

        self.points = []

        self.convex_polygons = []

    def decompose(self):
        del self.convex_polygons[:]
        self.convex_polygons = self.decomposer.decompose(self.points)

    def draw(self, painter):

        painter.save()
        painter.setPen(QPen(QBrush(QColor(232, 109, 21) if self.state is self.add_point else
                                   QColor(21, 144, 232)),
                            1,
                            Qt.SolidLine))
        painter.drawPolygon(QPolygon(self.points))

        for i, poly in enumerate(self.convex_polygons):
            if poly:
                painter.setPen(QPen(QBrush(Figure.COLORS[i % len(Figure.COLORS)]),
                                    2,
                                    Qt.SolidLine))
                painter.drawPolygon(QPolygon(poly))

        for point in self.points:
            painter.setPen(QPen(QBrush(QColor(31, 174, 222) if point is self.points[0] else
                                       QColor(222, 79, 31) if point is self.points[-1] else
                                       QColor(78, 222, 31)),
                                2,
                                Qt.SolidLine))
            painter.drawEllipse(point, Figure.CTRL_RADIUS, Figure.CTRL_RADIUS)

        Figure.draw(self, painter)
        painter.restore()

    def getDict(self):
        return {'polygon': {'editor': [qpoint2dict(point) for point in self.points],
                            'convex': [[qpoint2dict(point) for point in convex] for convex in self.convex_polygons]}}

    @staticmethod
    def fromDict(dictionary):
        polygon = Polygon()
        polygon.points = [dict2qpoint(d) for d in dictionary['editor']]
        polygon.decompose()
        polygon.state = polygon.control
        return polygon

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Polygon(' + ('{}' * len(self.points)).format(*[qpoint2str(point) for point in self.points]) + ')'
