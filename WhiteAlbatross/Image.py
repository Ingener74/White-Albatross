# encoding: utf8
from PySide.QtCore import QDir
from PySide.QtGui import QImage


class Image(object):
    def __init__(self, directory, file_name):
        self.directory = directory
        self.file_name = file_name
        self.figures = []

    def draw(self, painter):
        qimage = QImage(self.directory.path() + QDir.separator() + self.file_name)
        painter.drawImage(0, 0, qimage)
        painter.drawRect(0, 0, qimage.width(), qimage.height())

        for figure in self.figures:
            if figure:
                figure.draw(painter)

    def getDict(self):
        return {
            'file_name': self.file_name,
            'figures': [figure.getDict() for figure in self.figures]
        }

    def addFigure(self, figure):
        self.figures.append(figure)
