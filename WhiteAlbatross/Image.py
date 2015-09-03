# encoding: utf8
from PySide.QtCore import QDir, QPoint
from PySide.QtGui import QImage

from WhiteAlbatross.Rectangle import Rectangle
from WhiteAlbatross.Circle import Circle
from WhiteAlbatross.Polygon import Polygon
from WhiteAlbatross.Tools import qpoint2dict, dict2qpoint


# noinspection PyPep8Naming
class Image(object):
    def __init__(self, directory, *args, **kwargs):
        self.directory = directory
        self.figures = []

        if 'json_dict' in kwargs:
            self.file_name = kwargs['json_dict']['file_name']

            if 'draw_scale' in kwargs['json_dict']:
                self.draw_scale = kwargs['json_dict']['draw_scale']
            else:
                self.draw_scale = 1.0

            if 'draw_offset' in kwargs['json_dict']:
                self.draw_offset = dict2qpoint(kwargs['json_dict']['draw_offset'])
            else:
                self.draw_offset = QPoint()

            self.figures = [Rectangle(figure=figure_dict['rect']) if figure_dict.keys()[0] == 'rect' else
                            Circle(figure=figure_dict['circle']) if figure_dict.keys()[0] == 'circle' else
                            Polygon(figure=figure_dict['polygon']) for figure_dict in kwargs['json_dict']['figures']]
        else:
            self.draw_scale = 1.0
            self.draw_offset = QPoint()
            self.file_name = kwargs['file_name']

        self.image = None

    def draw(self, painter):
        painter.drawImage(0, 0, self.image)
        painter.drawRect(0, 0, self.image.width(), self.image.height())

        for figure in self.figures:
            if figure:
                figure.draw(painter, self.draw_scale)

    def getDict(self):
        return {
            'file_name': self.file_name,
            'draw_scale': self.draw_scale,
            'draw_offset': qpoint2dict(self.draw_offset),
            'figures': [figure.getDict() for figure in self.figures]
        }

    def addFigure(self, figure):
        self.figures.append(figure)

    def loadImage(self):
        self.image = QImage(self.directory.path() + QDir.separator() + self.file_name)

    def unloadImage(self):
        self.image = None
