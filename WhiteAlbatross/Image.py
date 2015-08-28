# encoding: utf8
from PySide.QtCore import QDir
from PySide.QtGui import QImage

from WhiteAlbatross.Rectangle import Rectangle
from WhiteAlbatross.Circle import Circle
from WhiteAlbatross.Polygon import Polygon


# noinspection PyPep8Naming
class Image(object):
    def __init__(self, directory, file_name, image_figures=None):
        self.directory = directory
        self.file_name = file_name
        self.figures = []
        if image_figures:
            self.figures = [Rectangle(figure=figure_dict['rect']) if figure_dict.keys()[0] == 'rect' else
                            Circle(figure=figure_dict['circle']) if figure_dict.keys()[0] == 'circle' else
                            Polygon(figure=figure_dict['polygon']) for figure_dict in image_figures]

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
