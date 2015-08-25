# encoding: utf8
import json
import os

from PySide.QtCore import Signal, QDir, QPoint, Qt
from PySide.QtGui import QWidget, QPainter, QSizePolicy, QPen, QColor, QTransform, QBrush, QImage, QPainterPath

from WhiteAlbatross.Image import Image
from WhiteAlbatross.Rectangle import Rectangle
from WhiteAlbatross.Circle import Circle
from WhiteAlbatross.Polygon import Polygon
from WhiteAlbatross.State import State


class FigureAdding(State):
    def __init__(self):
        State.__init__(self)

    def mouseDown(self, machine, *args, **kwargs):
        point = kwargs.get('point')
        if machine.image:
            # проходим по фигурам в изображении
            for figure in machine.image.figures:
                # если какая либо фигура отработала нажатие ...
                if figure.mouseDown(*args, **kwargs):
                    # ... дальше завершаем обход
                    break
            else:
                new_figure = WhiteAlbatrossWidget.FIGURE_TYPES[machine.type]()
                new_figure.mouseDown(point)
                machine.image.addFigure(new_figure)
                machine.figuresChanged.emit(machine.image.figures)
            machine.update()
        return False

    def mouseMove(self, machine, *args, **kwargs):
        point = kwargs.get('point')
        if machine.image:
            for figure in machine.image.figures:
                figure.mouseMove(*args, **kwargs)
            machine.update()

    def mouseUp(self, machine, *args, **kwargs):
        point = kwargs.get('point')
        if machine.image:
            for figure in machine.image.figures:
                figure.mouseUp(*args, **kwargs)
            machine.update()
            machine.figuresChanged.emit(machine.image.figures)

    def draw(self, painter):
        pass


class MovingImage(State):
    def __init__(self):
        State.__init__(self)
        self.start = QPoint(0, 0)

        self.old_offset = QPoint()

    def mouseDown(self, machine, *args, **kwargs):
        point = kwargs.get('point')
        self.start = point * machine.scale + machine.offset
        self.old_offset = machine.offset
        return False

    def mouseMove(self, machine, *args, **kwargs):
        point = kwargs.get('point')
        machine.offset = self.old_offset + ((point * machine.scale + machine.offset) - self.start)
        machine.update()
        pass

    def mouseUp(self, machine, *args, **kwargs):
        point = kwargs.get('point')
        machine.offset = self.old_offset + ((point * machine.scale + machine.offset) - self.start)
        machine.update()
        pass

    def draw(self, painter):
        pass


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

        self.offset = QPoint()
        self.scale = 1.0

        self.figure_adding = FigureAdding()
        self.moving_image = MovingImage()
        self.state = self.figure_adding

    def get_point(self, point):
        return point / self.scale - self.offset

    def mousePressEvent(self, e):
        if e.button() is Qt.MidButton or e.button() is Qt.MiddleButton:
            self.state = self.moving_image
        else:
            self.state = self.figure_adding

        self.state.mouseDown(self, point=self.get_point(e.pos()))

    def mouseMoveEvent(self, e):
        self.state.mouseMove(self, point=self.get_point(e.pos()))

    def mouseReleaseEvent(self, e):
        self.state.mouseUp(self, point=self.get_point(e.pos()))

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

        painter.setTransform(QTransform().scale(self.scale, self.scale).translate(self.offset.x(), self.offset.y()))
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
            try:
                with open(json_file_name) as f:
                    self.images = [Image(self.directory, image['file_name'], image['figures']) for image in json.load(f)]
            except ValueError, e:
                self.images = [Image(self.directory, image) for image in images]
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
            del self.image.figures[index:index+1]
            self.figuresChanged.emit(self.image.figures)
            self.update()
