# encoding: utf8
from PySide.QtCore import QDir
from PySide.QtGui import QImage

from WhiteAlbatross.Rectangle import Rectangle
from WhiteAlbatross.Circle import Circle
from WhiteAlbatross.Polygon import Polygon


# noinspection PyPep8Naming
class Image(object):
    def __init__(self, directory, file_name, json_dict=None):
        self.directory = directory
        self.file_name = file_name
        self.figures = [Rectangle.fromDict(js_dictionary['rect']) if js_dictionary.keys()[0] == 'rect' else
                        Circle.fromDict(js_dictionary['circle']) if js_dictionary.keys()[0] == 'circle' else
                        Polygon.fromDict(js_dictionary['polygon']) for js_dictionary in json_dict]

        pass

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
