# encoding: utf8
import sys

from PySide.QtCore import Qt, QSettings, QDir, QDirIterator
from PySide.QtGui import QApplication, QWidget, QFileDialog, QImage

from WhiteAlbatross import WhiteAlbatrossWidget
from GhastlyLion import Ui_GhastlyLion

COMPANY = 'Venus.Games'
APPNAME = 'GhastlyLion'


# Aberrant Tiger


class Image(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def get_qimage(self):
        return QImage(self.file_name)


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
        self.imagesList.itemClicked.connect(self.item_clicked)

        self.type.currentIndexChanged.connect(self.white_albatross.setType)

        self.images_list = []

    def add_images_click(self):
        file_names, selected_filters = QFileDialog.getOpenFileNames(parent=self,
                                                                    caption=u'Add image files to polygon list')
        print file_names, selected_filters

    def open_folder(self):
        directory = QFileDialog.getExistingDirectory(parent=self,
                                                     caption=u'Add images from directory')
        folder = QDir(directory)
        folder.setNameFilters(['*.png'])
        folder.setFilter(QDir.Files or QDir.NoDotAndDotDot)

        dir_iterator = QDirIterator(folder, flags=QDirIterator.Subdirectories, filters=QDir.Files)

        images = []

        while dir_iterator.hasNext():
            images.append(dir_iterator.next())

        self.images_list = [Image(image) for image in images]

        self.imagesList.clear()
        self.imagesList.addItems(images)

    def remove_images(self):
        pass

    def images_removed(self, *args, **kwargs):
        if self.images_list.rowCount() == 0:
            self.removeImages.setEnabled(False)
        else:
            self.removeImages.setEnabled(True)

    def save_button(self):
        print 'Save'

    def item_clicked(self, item):
        it = self.imagesList.indexFromItem(item).row()
        self.white_albatross.setImage(self.images_list[it])

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, e):
        self.settings.setValue(self.__class__.__name__, self.saveGeometry())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
