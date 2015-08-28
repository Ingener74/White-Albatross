# encoding: utf8
from PySide.QtCore import Qt, QPoint
from PySide.QtGui import QPolygon, QPen, QColor, QBrush

from WhiteAlbatross.Figure import Figure
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

    def mouseDown(self, machine, *args, **kwargs):
        point = kwargs.get('point')
        # Если нажатие в какой нибудь точке кроме последней то просто ничего не делаем и выходим
        for p in machine.points:
            if Figure.pointIsControl(p, point) and p is not machine.points[-1]:
                return True  # новую фигуру добавлять не надо

        # Если у нас больше 1 точки и мы тыкаем в последнюю тогда ...
        if len(machine.points) > 1 and Figure.pointIsControl(machine.points[-1], point):
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

    def mouseDown(self, machine, *args, **kwargs):
        for p in machine.points:
            if Figure.pointIsControl(p, kwargs['point']):
                if 'event' in kwargs and kwargs['event'].button() is Qt.RightButton:
                    del machine.points[machine.points.index(p)]
                    machine.decompose()
                    if len(machine.points) < 3:
                        machine.state = machine.delete
                else:
                    self.control1 = p
                return True
        return False

    def mouseMove(self, machine, *args, **kwargs):
        point = kwargs.get('point')
        if self.control1:
            self.control1.setX(point.x())
            self.control1.setY(point.y())

    def mouseUp(self, machine, *args, **kwargs):
        if self.control1:
            # Разбиение
            machine.decompose()

        self.control1 = None

    def draw(self, painter):
        if self.control1:
            painter.drawEllipse(self.control1, Figure.CTRL_RADIUS + 4, Figure.CTRL_RADIUS + 4)


# noinspection PyPep8Naming
class Polygon(Figure):
    def __init__(self, *args, **kwargs):

        self.add_point = AddPoint()
        self.control = Control()

        Figure.__init__(self, self.add_point)

        self.decomposer = BayazitDecomposer()

        self.points = []
        self.convex_polygons = []

        if 'figure' in kwargs:
            self.points = [dict2qpoint(p) for p in kwargs['figure']['editor']]
            self.decompose()
            self.state = self.control

        if len(args) > 0:
            self.points = args

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

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Polygon(' + ('{}' * len(self.points)).format(*[qpoint2str(point) for point in self.points]) + ')'
