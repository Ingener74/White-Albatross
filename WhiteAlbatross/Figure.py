# encoding: utf8
import math


def distance(point1, point2):
    return math.sqrt(math.pow(point2.y() - point1.y(), 2) +
                     math.pow(point2.x() - point1.x(), 2))


# noinspection PyPep8Naming
class Figure(object):
    CTRL = 13

    MODE_CONTROL = 0
    MODE_NORMAL = 1

    def __init__(self, state):
        self.mode = Figure.MODE_NORMAL
        self.state = state

    def getMode(self):
        return self.mode

    def setMode(self, mode):
        self.mode = mode

    def setPoint1(self, point):
        raise NotImplementedError

    def setPoint2(self, point):
        raise NotImplementedError

    def inSide(self, point):
        raise NotImplementedError

    def isControlPoint(self, point):
        raise NotImplementedError

    def moveControlPoint(self, point):
        raise NotImplementedError

    # new mouse control
    def mouseDown(self, point):
        self.state.mouseDown(point, self)

    def mouseMove(self, point):
        self.state.mouseMove(point, self)

    def mouseUp(self, point):
        self.state.mouseUp(point, self)

    def draw(self, painter):
        raise NotImplementedError

    def getDict(self):
        raise NotImplementedError
