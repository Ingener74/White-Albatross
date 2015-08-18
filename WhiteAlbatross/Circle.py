# encoding: utf8

from PySide.QtCore import QPoint

from WhiteAlbatross.Figure import distance, Figure
from WhiteAlbatross.State import State


class FirstPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, point, machine):
        machine.center = point
        machine.state = SecondPoint()
        return True


class SecondPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, point, machine):
        machine.ctrl = point
        return True

    def mouseMove(self, point, machine):
        machine.ctrl = point

    def mouseUp(self, point, machine):
        machine.ctrl = point
        if distance(machine.center, point) > Figure.CTRL:
            machine.state = Control()


class Control(State):
    def __init__(self):
        State.__init__(self)
        self.point = None

    def mouseDown(self, point, machine):
        if distance(machine.center, point) < Figure.CTRL:
            self.point = machine.center
        if distance(machine.ctrl, point) < Figure.CTRL:
            self.point = machine.ctrl
        if self.point:
            self.point.setX(point.x())
            self.point.setY(point.y())
            return True
        else:
            return False

    def mouseMove(self, point, machine):
        if self.point:
            self.point.setX(point.x())
            self.point.setY(point.y())

    def mouseUp(self, point, machine):
        self.point = None


# noinspection PyPep8Naming
class Circle(Figure):
    def __init__(self, x=0, y=0, radius=0):
        Figure.__init__(self, FirstPoint())
        self.center = QPoint(x, y)
        self.ctrl = QPoint(x + radius, y)

    def draw(self, painter):
        if not self.center.isNull() and not self.ctrl.isNull():
            radius = distance(self.center, self.ctrl)
            painter.drawEllipse(self.center, radius, radius)
            painter.drawEllipse(self.center, Figure.CTRL, Figure.CTRL)
            painter.drawEllipse(self.ctrl, Figure.CTRL, Figure.CTRL)

    def getDict(self):
        return {
            'circle': {
                'x': self.center.x(),
                'y': self.center.y(),
                'radius': distance(self.center, self.ctrl)
            }
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Circle(({x}, {y}), {radius})'.format(x=self.center.x(),
                                                     y=self.center.y(),
                                                     radius=distance(self.center, self.ctrl))
