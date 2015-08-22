# encoding: utf8

from PySide.QtCore import QPoint

from WhiteAlbatross.Figure import distance, Figure
from WhiteAlbatross.State import State


class FirstPoint(State):
    """
    Состояние для установки первой точки
    """

    def __init__(self):
        State.__init__(self)

    def mouseDown(self, event, machine):
        machine.center = event.pos()
        machine.state = machine.second_point
        return True


class SecondPoint(State):
    """
    Состояние для установки второй точки
    """

    def __init__(self):
        State.__init__(self)

    def mouseDown(self, event, machine):
        machine.ctrl = event.pos()
        return True

    def mouseMove(self, event, machine):
        machine.ctrl = event.pos()

    def mouseUp(self, event, machine):
        machine.ctrl = event.pos()
        if distance(machine.center, event.pos()) > Figure.CTRL_RADIUS:
            machine.state = machine.control


class Control(State):
    """
    Состояние для перемещения точек круга
    """

    def __init__(self):
        State.__init__(self)
        self.point = None

    def mouseDown(self, event, machine):
        if distance(machine.center, event.pos()) < Figure.CTRL_RADIUS:
            self.point = machine.center
        if distance(machine.ctrl, event.pos()) < Figure.CTRL_RADIUS:
            self.point = machine.ctrl

        if self.point and self.point == machine.center:
            delta = event.pos() - machine.center
            machine.center += delta
            machine.ctrl += delta
            return True
        elif self.point and self.point == machine.ctrl:
            machine.ctrl.setX(event.pos().x())
            machine.ctrl.setY(event.pos().y())
            return True
        else:
            return False

    def mouseMove(self, event, machine):
        if self.point and self.point == machine.center:
            delta = event.pos() - machine.center
            machine.center += delta
            machine.ctrl += delta
        elif self.point and self.point == machine.ctrl:
            machine.ctrl.setX(event.pos().x())
            machine.ctrl.setY(event.pos().y())

    def mouseUp(self, event, machine):
        self.point = None


# noinspection PyPep8Naming
class Circle(Figure):
    def __init__(self, center=QPoint(), ctrl=QPoint()):
        self.first_point = FirstPoint()
        self.second_point = SecondPoint()
        self.control = Control()

        Figure.__init__(self, self.first_point)
        self.center = center
        self.ctrl = ctrl

    def draw(self, painter):
        if not self.center.isNull() and not self.ctrl.isNull():
            radius = distance(self.center, self.ctrl)
            painter.drawEllipse(self.center, radius, radius)
            painter.drawEllipse(self.center, Figure.CTRL_RADIUS, Figure.CTRL_RADIUS)
            painter.drawEllipse(self.ctrl, Figure.CTRL_RADIUS, Figure.CTRL_RADIUS)

        Figure.draw(self, painter)

    def getDict(self):
        return {
            'circle': {
                'center': {
                    'x': self.center.x(),
                    'y': self.center.y(),
                },
                'ctrl': {
                    'x': self.ctrl.x(),
                    'y': self.ctrl.y(),
                }
            }
        }

    @staticmethod
    def fromDict(dictionary):
        circle = Circle(QPoint(dictionary['center']['x'],
                               dictionary['center']['y']),
                        QPoint(dictionary['ctrl']['x'],
                               dictionary['ctrl']['y']))
        circle.state = circle.control
        return circle

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Circle(({x}, {y}), {radius})'.format(x=self.center.x(),
                                                     y=self.center.y(),
                                                     radius=distance(self.center, self.ctrl))
