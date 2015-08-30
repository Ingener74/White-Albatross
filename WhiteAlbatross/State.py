# encoding: utf8


# noinspection PyPep8Naming
class State(object):
    def __init__(self):
        pass

    def mouseDown(self, machine, *args, **kwargs):
        return False

    def mouseMove(self, machine, *args, **kwargs):
        pass

    def mouseUp(self, machine, *args, **kwargs):
        pass

    def wheelEvent(self, machine, *args, **kwargs):
        pass

    def draw(self, painter, scale):
        pass
