import sys
import threading
from functools import partial

import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets

from MCT.player import Player
from MCT.websocket import Websocket_connection

VERSION = "1.0"

class AppWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Minimal Casting Tool (v{VERSION})")
        self.setWindowIcon(QtGui.QIcon('src/Icon.ico'))
        self.setGeometry(0, 0, 530, 150)
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() -
                  QtCore.QPoint(int(self.width() / 2), self.height()))

        # Attributes
        self.players = []
        self.connection = Websocket_connection()

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)

        # Players
        players_frame = QtWidgets.QFrame(self)
        self.layout.addWidget(players_frame)
        self.player_layout = QtWidgets.QVBoxLayout()
        self.player_layout.setAlignment(QtCore.Qt.AlignTop)
        players_frame.setLayout(self.player_layout)
        self.add_player()
        self.add_player()

        # Add player button
        bottom_frame = QtWidgets.QFrame()
        self.layout.addWidget(bottom_frame)
        bottom_layout = QtWidgets.QGridLayout()
        bottom_frame.setLayout(bottom_layout)

        add_player_button = QtWidgets.QPushButton()
        add_player_button.setMaximumWidth(100)
        add_player_button.setText("Add player")
        bottom_layout.addWidget(add_player_button, 0, 1, 1, 3)
        add_player_button.clicked.connect(self.add_player)

        # Info button
        info_button = QtWidgets.QPushButton()
        info_button.setMaximumWidth(30)
        bottom_layout.addWidget(info_button, 0, 4, 1, 1)
        info_button.clicked.connect(self.show_info)
        # info_button.setStyleSheet("border :0px")
        info_button.setIcon(self.style().standardIcon(
            getattr(QtWidgets.QStyle, 'SP_MessageBoxInformation')))

        # Start connection
        self.start_websocket()

    def add_player(self):
        player_index = len(self.players)
        self.players.append(Player(player_index))
        self.player_layout.addWidget(self.players[-1])
        self.players[-1].btn_remove.clicked.connect(
            partial(self.remove_player, self.players[-1]))
        self.players[-1].data_changed.connect(self.player_data_changed)

    def remove_player(self, player_frame):
        self.player_layout.removeWidget(player_frame)
        self.players.remove(player_frame)
        player_frame.deleteLater()
        self.resize(self.width(), self.layout.sizeHint().height())

    def start_websocket(self):
        self.thread_server = threading.Thread(target=self.connection.run,
                                              daemon=True)
        self.thread_server.start()

    def player_data_changed(self):
        data = []
        for player in self.players:
            data.append(player.get_data())
        self.connection.send(data)

    def show_info(self):
        webbrowser.open("https://www.maguro.one/")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = AppWindow()
    MainWindow.show()
    sys.exit(app.exec_())
