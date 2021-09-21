import sys
import webbrowser
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

import MCT.helper_functions as HF
from MCT.main_widget import MainWidget

VERSION = "1.01"


class MainApp(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(f"Minimal Casting Tool (v{VERSION})")
        self.setWindowIcon(QtGui.QIcon(HF.inner('src/Icon.ico')))
        self.setGeometry(0, 0, 530, 150)
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() -
                  QtCore.QPoint(int(self.width() / 2), self.height()))

        # Create central widget
        self.setCentralWidget(MainWidget())

        ### Create menu bar items
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        link_menu = menubar.addMenu('Links')

        # Exit
        icon = self.style().standardIcon(
            getattr(QtWidgets.QStyle, 'SP_DialogCloseButton'))
        exitAction = QtWidgets.QAction(icon, 'Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        file_menu.addAction(exitAction)

        # Github
        icon = QtGui.QIcon(HF.inner("src/github.png"))
        githubAction = QtWidgets.QAction(icon, 'Github page', self)
        githubAction.triggered.connect(
            partial(webbrowser.open,
                    "https://github.com/FluffyMaguro/mini-casting-tool"))
        link_menu.addAction(githubAction)

        # Maguro
        icon = QtGui.QIcon(HF.inner("src/maguro.jpg"))
        maguroAction = QtWidgets.QAction(icon, 'Maguro.one', self)
        maguroAction.triggered.connect(
            partial(webbrowser.open, "https://www.maguro.one/"))
        link_menu.addAction(maguroAction)

        self.statusBar()
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec_())
