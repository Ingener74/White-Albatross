# encoding: utf8
from PySide.QtGui import QWidget, QPainter, QSizePolicy, QPen, QColor

from WhiteAlbatross import Rectangle, Circle, Polygon


class WhiteAlbatrossWidget(QWidget):
    """
    Виджет рисования физических форм для Box2D по изображению
    """
    # POLYGON = 0
    # RECTANGLE = 1
    # CIRCLE = 2

    FIGURE_TYPES = (Polygon.Polygon,
                    Rectangle.Rectangle,
                    Circle.Circle)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.type = 0

        self.images = []

        self.image = None
        self.figure = None

    def mousePressEvent(self, e):
        self.figure = WhiteAlbatrossWidget.FIGURE_TYPES[self.type]()
        if self.figure:
            self.figure.setPoint1(e.pos())

    def mouseMoveEvent(self, e):
        if self.figure:
            self.figure.setPoint2(e.pos())
            self.update()

    def mouseReleaseEvent(self, e):
        if self.figure:
            self.figure.setPoint2(e.pos())
            self.update()
        if self.image:
            self.image.addFigure(self.figure)
        self.figure = None

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.image is not None:
            old_pen = painter.pen()

            new_pen = QPen()
            new_pen.setColor(QColor(0, 150, 0))
            painter.setPen(new_pen)

            self.image.draw(painter)

            painter.setPen(old_pen)

        if self.figure:
            self.figure.draw(painter)

        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def setImage(self, image):
        """
        Устанавливает изображение для фона
        :param image: Изображение
        """
        self.image = image
        self.update()

    def getPolygons(self):
        """
        Возвращает подсчитанные полигоны
        :return:
        """
        pass

    def setType(self, type):
        self.type = type
