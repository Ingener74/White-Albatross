# encoding: utf8
from PySide.QtCore import QRect, QPoint
from PySide.QtGui import QPainterPath, QPen, QBrush, QColor

from WhiteAlbatross.Figure import distance, Figure
from WhiteAlbatross.State import State


class FirstPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, point, machine):
        machine.p1 = point
        machine.state = SecondPoint()
        return True

    def mouseMove(self, point, machine):
        pass

    def mouseUp(self, point, machine):
        pass


class SecondPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, point, machine):
        machine.p2 = point
        return True

    def mouseMove(self, point, machine):
        machine.p2 = point

    def mouseUp(self, point, machine):
        machine.p2 = point
        if distance(machine.p1, point) > Figure.CTRL:
            machine.state = Control()


class Control(State):
    def __init__(self):
        State.__init__(self)
        self.point = None

    def mouseDown(self, point, machine):
        # if distance(poi)
        return True

    def mouseMove(self, point, machine):
        if self.point:
            self.point = point

    def mouseUp(self, point, machine):
        self.point = None


# noinspection PyPep8Naming
class Rectangle(Figure):
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        Figure.__init__(self, FirstPoint())
        self.p1 = QPoint(x1, y1)
        self.p2 = QPoint(x2, y2)

    def draw(self, painter):

        # brush = QBrush()
        # brush.setColor(QColor(0, 100, 0, 100))
        # painter.setBrush(brush)
        #
        # painter_path = QPainterPath()
        # painter_path.addRect(self.x1, self.y1, self.x2, self.y2)
        # painter.drawPath(painter_path)

        if self.p1.x() and self.p1.y() and self.p2.x() and self.p2.y():
            painter.drawRect(QRect(self.p1, self.p2))
            painter.drawEllipse(self.p1.x() - Figure.CTRL / 2, self.p1.y() - Figure.CTRL / 2, Figure.CTRL, Figure.CTRL)
            painter.drawEllipse(self.p2.x() - Figure.CTRL / 2, self.p2.y() - Figure.CTRL / 2, Figure.CTRL, Figure.CTRL)

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
