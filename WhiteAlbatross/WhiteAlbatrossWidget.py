# encoding: utf8
import json

from PySide.QtCore import Signal, QDir
from PySide.QtGui import QWidget, QPainter, QSizePolicy, QPen, QColor, QTransform, QBrush, QImage, QPainterPath

from WhiteAlbatross.Image import Image
from WhiteAlbatross.Figure import Figure
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
            for figure in self.image.figures:
                if figure.mouseDown(e.pos()):
                    break
            else:
                new_figure = WhiteAlbatrossWidget.FIGURE_TYPES[self.type]()
                new_figure.mouseDown(e.pos())
                self.image.addFigure(new_figure)
                self.figuresChanged.emit(self.image.figures)
            self.update()

    def mouseMoveEvent(self, e):
        if self.image:
            for figure in self.image.figures:
                figure.mouseMove(e.pos())
            self.update()

    def mouseReleaseEvent(self, e):
        if self.image:
            for figure in self.image.figures:
                figure.mouseUp(e.pos())
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
        self.images = [Image(self.directory, image) for image in images]

    def selectImage(self, index):
        """
        Устанавливает изображение для фона
        :param image: Изображение
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

    def setType(self, type):
        self.type = type

    def deleteFigure(self, index):
        if self.image:
            del self.image.figures[index]