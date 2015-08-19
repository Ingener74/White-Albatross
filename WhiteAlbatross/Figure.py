# encoding: utf8
import math


def distance(point1, point2):
    return math.sqrt(math.pow(point2.y() - point1.y(), 2) +
                     math.pow(point2.x() - point1.x(), 2))


# noinspection PyPep8Naming
class Figure(object):
    CTRL_RADIUS = 7

    def __init__(self, state):
        self.state = state

    def mouseDown(self, point):
        return self.state.mouseDown(point, self)

    def mouseMove(self, point):
        self.state.mouseMove(point, self)

    def mouseUp(self, point):
        self.state.mouseUp(point, self)

    def draw(self, painter):
        raise NotImplementedError

    def getDict(self):
        raise NotImplementedError
