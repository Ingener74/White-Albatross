# encoding: utf8
import json
import os

from PySide.QtCore import Signal, QDir
from PySide.QtGui import QWidget, QPainter, QSizePolicy, QPen, QColor, QTransform, QBrush, QImage, QPainterPath

from WhiteAlbatross.Image import Image
from WhiteAlbatross.Rectangle import Rectangle
from WhiteAlbatross.Circle import Circle
from WhiteAlbatross.Polygon import Polygon


# noinspection PyPep8Naming
class WhiteAlbatrossWidget(QWidget):
    """
    Виджет рисования физических форм для Box2D по изображению
    """

    figuresChanged = Signal(object)

    FIGURE_TYPES = (Polygon,
                    Rectangle,
                    Circle)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.directory = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.type = 0

        self.images = []

        self.image = None
        self.scale = 1.0

    def mousePressEvent(self, e):
        if self.image:
            # проходим по фигурам в изображении
            for figure in self.image.figures:
                # если какая либо фигура отработала нажатие ...
                if figure.mouseDown(e):
                    # ... дальше завершаем обход
                    break
            else:
                new_figure = WhiteAlbatrossWidget.FIGURE_TYPES[self.type]()
                new_figure.mouseDown(e)
                self.image.addFigure(new_figure)
                self.figuresChanged.emit(self.image.figures)
            self.update()

    def mouseMoveEvent(self, e):
        if self.image:
            for figure in self.image.figures:
                figure.mouseMove(e)
            self.update()

    def mouseReleaseEvent(self, e):
        if self.image:
            for figure in self.image.figures:
                figure.mouseUp(e)
            self.update()
            self.figuresChanged.emit(self.image.figures)

    def wheelEvent(self, e):
        self.scale += e.delta() / 1200.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Фон
        painter_path = QPainterPath()
        painter_path.addRect(0, 0, self.width() - 1, self.height() - 1)
        painter.fillPath(painter_path,
                         QBrush(QImage(':/main/background.png')))

        painter.setTransform(QTransform().scale(self.scale, self.scale))
        if self.image:
            old_pen = painter.pen()

            new_pen = QPen()
            new_pen.setColor(QColor(0, 150, 0))
            painter.setPen(new_pen)

            self.image.draw(painter)

            painter.setPen(old_pen)

    def addImages(self, directory, images):
        self.directory = directory

        json_file_name = self.directory.path() + QDir.separator() + 'box2d.json'

        if os.path.exists(json_file_name):
            with open(json_file_name) as f:
                self.images = [Image(self.directory, image['file_name'], image['figures']) for image in json.load(f)]
        else:
            self.images = [Image(self.directory, image) for image in images]

    def selectImage(self, index):
        """
        Выбираем изображение для фона
        :param index: Изображение
        """
        self.image = self.images[index]
        if self.image:
            self.figuresChanged.emit(self.image.figures)
        self.update()

    def getPolygons(self):
        """
        Возвращает подсчитанные полигоны
        :return:
        """
        pass

    def save(self):
        with open(self.directory.path() + QDir.separator() + 'box2d.json', 'w') as js:
            figures_ = [image.getDict() for image in self.images]
            json.dump(obj=figures_, fp=js, separators=(',', ':'), indent=4)

    def setType(self, figure_type):
        self.type = figure_type

    def deleteFigure(self, index):
        if self.image:
            del self.image.figures[index]
