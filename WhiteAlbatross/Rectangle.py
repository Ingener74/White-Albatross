# encoding: utf8
from PySide.QtCore import (QRect, QPoint, Qt)
from PySide.QtGui import (QPen, QBrush, QColor)

from WhiteAlbatross.Figure import Figure
from WhiteAlbatross.State import State


class FirstPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, machine, *args, **kwargs):
        machine.p1 = kwargs['point']
        machine.state = machine.second_point
        return True


class SecondPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, machine, *args, **kwargs):
        machine.p2 = kwargs['point']
        return True

    def mouseMove(self, machine, *args, **kwargs):
        machine.p2 = kwargs['point']

    def mouseUp(self, machine, *args, **kwargs):
        machine.p2 = kwargs['point']
        if not Figure.pointIsControl(machine.p1, kwargs['point'], kwargs['scale']):
            machine.state = machine.control


class Control(State):
    def __init__(self):
        State.__init__(self)
        self.point = None

    def mouseDown(self, machine, *args, **kwargs):
        point = kwargs['point']
        if Figure.pointIsControl(machine.p1, point, kwargs['scale']):
            self.point = machine.p1
        if Figure.pointIsControl(machine.p2, point, kwargs['scale']):
            self.point = machine.p2

        if self.point:
            if 'event' in kwargs and kwargs['event'].button() == Qt.RightButton:
                machine.state = machine.delete
            else:
                self.point.setX(point.x())
                self.point.setY(point.y())
            return True
        else:
            return False

    def mouseMove(self, machine, *args, **kwargs):
        point = kwargs['point']
        if self.point:
            self.point.setX(point.x())
            self.point.setY(point.y())

    def mouseUp(self, machine, *args, **kwargs):
        self.point = None

    def draw(self, painter, scale):
        if self.point:
            pen = QPen()
            pen.setColor(QColor(255, 0, 0))
            painter.setPen(pen)
            painter.drawEllipse(self.point, Figure.CTRL_RADIUS + 4, Figure.CTRL_RADIUS + 4)


# noinspection PyPep8Naming
class Rectangle(Figure):
    def __init__(self, *args, **kwargs):

        self.first_point = FirstPoint()
        self.second_point = SecondPoint()
        self.control = Control()

        self.p1 = QPoint()
        self.p2 = QPoint()

        Figure.__init__(self, self.first_point)
        if 'x1' in kwargs and 'y1' in kwargs:
            self.p1 = QPoint(kwargs['x1'], kwargs['y1'])
        if 'x2' in kwargs and 'y2' in kwargs:
            self.p2 = QPoint(kwargs['x2'], kwargs['y2'])
        if 'p1' in kwargs:
            self.p1 = kwargs['p1']
        if 'p2' in kwargs:
            self.p2 = kwargs['p2']
        if len(args) == 2:
            self.p1 = args[0]
            self.p2 = args[1]
        if len(args) == 4:
            self.p1 = QPoint(args[0], args[1])
            self.p2 = QPoint(args[2], args[3])

        if 'figure' in kwargs:
            self.p1 = QPoint(kwargs['figure']['x1'], kwargs['figure']['y1'])
            self.p2 = QPoint(kwargs['figure']['x2'], kwargs['figure']['y2'])
            self.state = self.control

    def draw(self, painter, scale):
        painter.save()
        if not self.p1.isNull() and not self.p2.isNull():
            painter.setPen(QPen(QBrush(QColor(232, 109, 21) if self.state is not self.control else
                                       QColor(21, 144, 232)),
                                self.lineWidth(scale),
                                Qt.SolidLine))
            painter.setBrush(QBrush(QColor(21, 144, 232, 150)))
            painter.drawRect(QRect(self.p1, self.p2))

            self.drawControlPoint(painter, self.p1, QColor(31, 174, 222), scale)
            self.drawControlPoint(painter, self.p2, QColor(222, 79, 31), scale)

        Figure.draw(self, painter, scale)
        painter.restore()

    def getDict(self):
        return {
            'rect': {
                'x1': self.p1.x(),
                'y1': self.p1.y(),
                'x2': self.p2.x(),
                'y2': self.p2.y()
            }
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Rectangle(({x1}, {y1}), ({x2}, {y2}))'.format(x1=self.p1.x(),
                                                              y1=self.p1.y(),
                                                              x2=self.p2.x(),
                                                              y2=self.p2.y())
