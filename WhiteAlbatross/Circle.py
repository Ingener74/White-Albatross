# encoding: utf8

from PySide.QtCore import QPoint, Qt
from PySide.QtGui import QPen, QColor
from PySide.QtGui import QBrush

from WhiteAlbatross.Figure import distance, Figure
from WhiteAlbatross.State import State


class FirstPoint(State):
    """
    Состояние для установки первой точки
    """

    def __init__(self):
        State.__init__(self)

    def mouseDown(self, machine, *args, **kwargs):
        point = kwargs['point']
        machine.center = point
        machine.state = machine.second_point
        return True


class SecondPoint(State):
    """
    Состояние для установки второй точки
    """

    def __init__(self):
        State.__init__(self)

    def mouseDown(self, machine, *args, **kwargs):
        point = kwargs['point']
        machine.ctrl = point
        return True

    def mouseMove(self, machine, *args, **kwargs):
        point = kwargs['point']
        machine.ctrl = point

    def mouseUp(self, machine, *args, **kwargs):
        point = kwargs['point']
        machine.ctrl = point
        if not Figure.pointIsControl(machine.center, point):
            machine.state = machine.control


class Control(State):
    """
    Состояние для перемещения точек круга
    """

    def __init__(self):
        State.__init__(self)
        self.point = None

    def mouseDown(self, machine, *args, **kwargs):
        point = kwargs['point']
        if Figure.pointIsControl(machine.center, point):
            self.point = machine.center
        if Figure.pointIsControl(machine.ctrl, point):
            self.point = machine.ctrl

        if self.point:
            if 'event' in kwargs and kwargs['event'].button() is Qt.RightButton:
                machine.state = machine.delete
            elif self.point == machine.center:
                delta = point - machine.center
                machine.center += delta
                machine.ctrl += delta
            elif self.point == machine.ctrl:
                machine.ctrl.setX(point.x())
                machine.ctrl.setY(point.y())
            return True
        else:
            return False

    def mouseMove(self, machine, *args, **kwargs):
        point = kwargs['point']
        if self.point and self.point == machine.center:
            delta = point - machine.center
            machine.center += delta
            machine.ctrl += delta
        elif self.point and self.point == machine.ctrl:
            machine.ctrl.setX(point.x())
            machine.ctrl.setY(point.y())

    def mouseUp(self, machine, *args, **kwargs):
        self.point = None


# noinspection PyPep8Naming
class Circle(Figure):
    def __init__(self, *args, **kwargs):
        self.first_point = FirstPoint()
        self.second_point = SecondPoint()
        self.control = Control()

        Figure.__init__(self, self.first_point)

        self.center = QPoint()
        self.ctrl = QPoint()

        if 'center' in kwargs:
            self.center = kwargs['center']
        if 'ctrl' in kwargs:
            self.ctrl = kwargs['ctrl']
        if 'figure' in kwargs:
            self.center = QPoint(kwargs['figure']['center']['x'],
                                 kwargs['figure']['center']['y'])
            self.ctrl = QPoint(kwargs['figure']['ctrl']['x'],
                               kwargs['figure']['ctrl']['y'])
            self.state = self.control
        if len(args) == 2:
            self.center = args[0]
            self.ctrl = args[1]
        if len(args) == 4:
            self.center = QPoint(args[0], args[1])
            self.ctrl = QPoint(args[2], args[3])

    def draw(self, painter):
        painter.save()
        if not self.center.isNull() and not self.ctrl.isNull():
            radius = distance(self.center, self.ctrl)
            painter.setPen(QPen(QBrush(QColor(232, 109, 21) if self.state is not self.control else
                                       QColor(21, 144, 232)),
                                2,
                                Qt.SolidLine))
            painter.drawEllipse(self.center, radius, radius)

            painter.setPen(QPen(QBrush(QColor(31, 174, 222)), 2, Qt.SolidLine))
            painter.drawEllipse(self.center, Figure.CTRL_RADIUS, Figure.CTRL_RADIUS)

            painter.setPen(QPen(QBrush(QColor(222, 79, 31)), 2, Qt.SolidLine))
            painter.drawEllipse(self.ctrl, Figure.CTRL_RADIUS, Figure.CTRL_RADIUS)

        Figure.draw(self, painter)
        painter.restore()

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

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Circle(({x}, {y}), {radius})'.format(x=self.center.x(),
                                                     y=self.center.y(),
                                                     radius=distance(self.center, self.ctrl))
