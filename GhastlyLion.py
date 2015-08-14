# encoding: utf8
import sys
from PySide.QtCore import Qt, QSettings
from PySide.QtGui import QApplication, QWidget, QPainter, QPolygon
from WhiteAlbatross import Point

COMPANY = 'Venus.Games'
APPNAME = 'GhastlyLion'


# Screaming Mercury
# Aberrant Tiger


class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
        self.restoreGeometry(self.settings.value(self.__class__.__name__))

        self.polygon = [Point(3, 4), Point(10, 20), Point(40, 10)]

    def paintEvent(self, *args, **kwargs):
        painter = QPainter(self)

        painter.drawPolygon(QPolygon([p.qpoint() for p in self.polygon]))

    def mousePressEvent(self, *args, **kwargs):
        pass

    def mouseMoveEvent(self, *args, **kwargs):
        pass

    def mouseReleaseEvent(self, *args, **kwargs):
        pass

    def keyPressEvent(self, *args, **kwargs):
        if args[0].key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, *args, **kwargs):
        self.settings.setValue(self.__class__.__name__, self.saveGeometry())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
