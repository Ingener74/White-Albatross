# encoding: utf8
from PySide.QtCore import QRect, QPoint
from PySide.QtGui import QPainterPath, QPen, QBrush, QColor

from WhiteAlbatross.Figure import distance, Figure
from WhiteAlbatross.State import State


class FirstPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, point, machine):
        machine.x1 = point.x()
        machine.y1 = point.y()
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
        machine.x2 = point.x()
        machine.y2 = point.y()
        return False

    def mouseMove(self, point, machine):
        machine.x2 = point.x()
        machine.y2 = point.y()

    def mouseUp(self, point, machine):
        machine.x2 = point.x()
        machine.y2 = point.y()
        machine.state = Control()


class Control(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, point, machine):
        return False

    def mouseMove(self, point, machine):
        pass

    def mouseUp(self, point, machine):
        pass


# noinspection PyPep8Naming
class Rectangle(Figure):
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        Figure.__init__(self, FirstPoint())
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def setPoint1(self, point):
        self.x1 = point.x()
        self.y1 = point.y()

    def setPoint2(self, point):
        self.x2 = point.x()
        self.y2 = point.y()
        return True

    def inSide(self, point):
        return max(self.x1, self.x2) > point.x() > min(self.x1, self.x2) and \
               max(self.y1, self.y2) > point.y() > min(self.y1, self.y2)

    def isControlPoint(self, point):
        dist1 = distance(QPoint(self.x1, self.y1), point)
        dist2 = distance(QPoint(self.x2, self.y2), point)
        return dist1 < Rectangle.CTRL or dist2 < Rectangle.CTRL

    def moveControlPoint(self, point):
        if self.mode is not Figure.MODE_CONTROL:
            return
        dist1 = distance(QPoint(self.x1, self.y1), point)
        dist2 = distance(QPoint(self.x2, self.y2), point)
        if dist1 < dist2:
            self.x1 = point.x()
            self.y1 = point.y()
        else:
            self.x2 = point.x()
            self.y2 = point.y()

    def draw(self, painter):

        # brush = QBrush()
        # brush.setColor(QColor(0, 100, 0, 100))
        # painter.setBrush(brush)
        #
        # painter_path = QPainterPath()
        # painter_path.addRect(self.x1, self.y1, self.x2, self.y2)
        # painter.drawPath(painter_path)

        if self.x1 and self.y1 and self.x2 and self.y2:
            painter.drawRect(QRect(QPoint(self.x1, self.y1), QPoint(self.x2, self.y2)))
            painter.drawEllipse(self.x1 - Rectangle.CTRL / 2, self.y1 - Rectangle.CTRL / 2, Rectangle.CTRL, Rectangle.CTRL)
            painter.drawEllipse(self.x2 - Rectangle.CTRL / 2, self.y2 - Rectangle.CTRL / 2, Rectangle.CTRL, Rectangle.CTRL)

    def getDict(self):
        return {
            'rect': {
                'x1': self.x1,
                'y1': self.y1,
                'x2': self.x2,
                'y2': self.y2
            }
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Rectangle(({x1}, {y1}), ({x2}, {y2}))'.format(x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2)
