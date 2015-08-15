# encoding: utf8
from PySide.QtGui import QWidget, QPainter, QPolygon, QSizePolicy

from WhiteAlbatross import Point


class WhiteAlbatrossWidget(QWidget):
    """
    Показывает изображение по которому рисуется контур
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.polygon = [Point(20, 20), Point(100, 200), Point(200, 100)]

    def mousePressEvent(self, *args, **kwargs):
        pass

    def mouseMoveEvent(self, *args, **kwargs):
        pass

    def mouseReleaseEvent(self, *args, **kwargs):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.drawPolygon(QPolygon([p.qpoint() for p in self.polygon]))

        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def setImage(self, image):
        """
        Устанавливает изображение для фона
        :param image: Изображение
        """
        pass

    def getPolygons(self):
        """
        Возвращает подсчитанные полигоны
        :return:
        """
        pass
