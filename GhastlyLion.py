# encoding: utf8
import sys

from PySide.QtCore import Qt, QSettings, QAbstractListModel

from PySide.QtGui import QApplication, QWidget, QFileDialog

from WhiteAlbatross import WhiteAlbatrossWidget
from GhastlyLion import Ui_GhastlyLion

COMPANY = 'Venus.Games'
APPNAME = 'GhastlyLion'


# Aberrant Tiger


class Image(object):
    def __init__(self):
        pass


class ImageFileList(QAbstractListModel):
    def __init__(self):
        QAbstractListModel.__init__(self)

        self.images = []

    def rowCount(self, *args, **kwargs):
        return len(self.images)


class MainWindow(QWidget, Ui_GhastlyLion):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
        self.restoreGeometry(self.settings.value(self.__class__.__name__))

        self.white_albatross = WhiteAlbatrossWidget()
        self.workLayout.insertWidget(1, self.white_albatross)

        self.save.clicked.connect(self.save_button)
        self.addImages.clicked.connect(self.add_images_click)
        self.openFolder.clicked.connect(self.open_folder)
        self.removeImages.clicked.connect(self.remove_images)

        self.images_list = ImageFileList()
        self.images_list.rowsRemoved.connect(self.images_removed)

        self.imagesList.setModel(self.images_list)

    def add_images_click(self):
        files = QFileDialog.getOpenFileNames(parent=self,
                                             caption=u'Add image files to polygon list')

        self.images_list.insertRow()

    def open_folder(self):
        pass

    def remove_images(self):
        pass

    def images_removed(self, *args, **kwargs):
        if self.images_list.rowCount() == 0:
            self.removeImages.setEnabled(False)
        else:
            self.removeImages.setEnabled(True)

    def save_button(self):
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
