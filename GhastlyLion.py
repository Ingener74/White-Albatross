# encoding: utf8
import sys

from PySide.QtCore import Qt, QSettings, QDir, QDirIterator
from PySide.QtGui import QApplication, QWidget, QFileDialog

from WhiteAlbatross import WhiteAlbatrossWidget
from GhastlyLion import Ui_GhastlyLion

SPLITTER = 'splitter'
LAST_FIGURE_TYPE = 'last_figure_type'
CURRENT_DIRECTORY = 'current_directory'

COMPANY = 'Venus.Games'
APPNAME = 'GhastlyLion'


class MainWindow(QWidget, Ui_GhastlyLion):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.current_directory = None

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
        self.restoreGeometry(self.settings.value(self.__class__.__name__))
        self.splitter.restoreState(self.settings.value(SPLITTER))
        self.current_directory = self.settings.value(CURRENT_DIRECTORY)

        self.white_albatross = WhiteAlbatrossWidget()
        self.white_albatross.figuresChanged.connect(self.on_figures_changed)
        self.workLayout.insertWidget(1, self.white_albatross)

        self.type.currentIndexChanged.connect(self.white_albatross.setType)
        self.type.setCurrentIndex(int(self.settings.value(LAST_FIGURE_TYPE, defaultValue=0)))

        self.save.clicked.connect(self.save_button)
        self.addImages.clicked.connect(self.add_images_click)
        self.openFolder.clicked.connect(self.open_folder)
        self.removeImages.clicked.connect(self.remove_images)
        self.imagesList.itemClicked.connect(self.item_clicked)

        self.figures.customContextMenuRequested.connect(self.figures_context_menu)

        if self.current_directory:
            self.open_folder()

    def add_images_click(self):
        file_names, selected_filters = QFileDialog.getOpenFileNames(parent=self,
                                                                    caption=u'Add image files to polygon list')
        print file_names, selected_filters

    def open_folder(self):
        if not self.current_directory:
            self.current_directory = QFileDialog.getExistingDirectory(parent=self,
                                                                      caption=u'Add images from directory')

        folder = QDir(self.current_directory)
        folder.setNameFilters(['*.png'])
        folder.setFilter(QDir.Files or QDir.NoDotAndDotDot)

        dir_iterator = QDirIterator(folder, flags=QDirIterator.Subdirectories, filters=QDir.Files)

        images = []

        while dir_iterator.hasNext():
            images.append(folder.relativeFilePath(dir_iterator.next()))

        self.white_albatross.addImages(folder, images)
        self.imagesList.addItems(images)

    def remove_images(self):
        pass

    def images_removed(self, *args, **kwargs):
        if self.images_list.rowCount() == 0:
            self.removeImages.setEnabled(False)
        else:
            self.removeImages.setEnabled(True)

    def save_button(self):
        self.white_albatross.save()

    def item_clicked(self, item):
        self.white_albatross.selectImage(self.imagesList.indexFromItem(item).row())

    def on_figures_changed(self, figures):
        self.figures.clear()
        self.figures.addItems([str(figure) for figure in figures])
        # self.white_albatross.save()

    def figures_context_menu(self, point):
        print point

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, e):
        self.settings.setValue(self.__class__.__name__, self.saveGeometry())
        self.settings.setValue(SPLITTER, self.splitter.saveState())
        self.settings.setValue(CURRENT_DIRECTORY, self.current_directory)
        self.settings.setValue(LAST_FIGURE_TYPE, self.type.currentIndex())


if __name__ == '__main__':
    # noinspection PyTypeChecker,PyCallByClass
    QApplication.setStyle(u'plastique')
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
