# encoding: utf8
from PySide.QtCore import QRect, QPoint, Qt
from PySide.QtGui import QPainterPath, QPen, QBrush, QColor

from WhiteAlbatross.Figure import distance, Figure
from WhiteAlbatross.State import State


class FirstPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, event, machine):
        machine.p1 = event.pos()
        machine.state = machine.second_point
        return True


class SecondPoint(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, event, machine):
        machine.p2 = event.pos()
        return True

    def mouseMove(self, event, machine):
        machine.p2 = event.pos()

    def mouseUp(self, event, machine):
        machine.p2 = event.pos()
        if distance(machine.p1, event.pos()) > Figure.CTRL_RADIUS:
            machine.state = machine.control


class Control(State):
    def __init__(self):
        State.__init__(self)
        self.point = None

    def mouseDown(self, event, machine):
        if distance(machine.p1, event.pos()) < Figure.CTRL_RADIUS:
            self.point = machine.p1
        if distance(machine.p2, event.pos()) < Figure.CTRL_RADIUS:
            self.point = machine.p2
        if self.point:
            self.point.setX(event.pos().x())
            self.point.setY(event.pos().y())
            return True
        else:
            return False

    def mouseMove(self, event, machine):
        if self.point:
            self.point.setX(event.pos().x())
            self.point.setY(event.pos().y())

    def mouseUp(self, event, machine):
        self.point = None

    def draw(self, painter):
        if self.point:
            pen = QPen()
            pen.setColor(QColor(255, 0, 0))
            painter.setPen(pen)
            painter.drawEllipse(self.point, Figure.CTRL_RADIUS + 4, Figure.CTRL_RADIUS + 4)


# noinspection PyPep8Naming
class Rectangle(Figure):
    def __init__(self, x1=0, y1=0, x2=0, y2=0):

        self.first_point = FirstPoint()
        self.second_point = SecondPoint()
        self.control = Control()

        Figure.__init__(self, self.first_point)
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

        painter.save()
        if not self.p1.isNull() and not self.p2.isNull():
            painter.setPen(QPen(QBrush(QColor(232, 109, 21) if self.state is not self.control else
                                       QColor(21, 144, 232)),
                                2,
                                Qt.SolidLine))
            painter.drawRect(QRect(self.p1, self.p2))

            painter.setPen(QPen(QBrush(QColor(31, 174, 222)), 2, Qt.SolidLine))
            painter.drawEllipse(self.p1, Figure.CTRL_RADIUS, Figure.CTRL_RADIUS)

            painter.setPen(QPen(QBrush(QColor(222, 79, 31)), 2, Qt.SolidLine))
            painter.drawEllipse(self.p2, Figure.CTRL_RADIUS, Figure.CTRL_RADIUS)

        Figure.draw(self, painter)
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

    @staticmethod
    def fromDict(dictionary):
        rect = Rectangle(dictionary['x1'], dictionary['y1'], dictionary['x2'], dictionary['y2'])
        rect.state = rect.control
        return rect

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Rectangle(({x1}, {y1}), ({x2}, {y2}))'.format(x1=self.p1.x(),
                                                              y1=self.p1.y(),
                                                              x2=self.p2.x(),
                                                              y2=self.p2.y())
