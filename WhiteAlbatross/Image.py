# encoding: utf8
from PySide.QtGui import QImage


class Image(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.figures = []

    def draw(self, painter):
        qimage = QImage(self.file_name)
        painter.drawImage(0, 0, qimage)
        painter.drawRect(0, 0, qimage.width(), qimage.height())

        for figure in self.figures:
            if figure:
                figure.draw(painter)

    def addFigure(self, figure):
        self.figures.append(figure)
