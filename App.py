import sys
import webbrowser
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

import MCT.helper_functions as HF
from MCT.player import Player
from MCT.websocket import Websocket_connection_manager

VERSION = "1.0"


class AppWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Minimal Casting Tool (v{VERSION})")
        self.setWindowIcon(QtGui.QIcon(HF.inner('src/Icon.ico')))
        self.setGeometry(0, 0, 530, 150)
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() -
                  QtCore.QPoint(int(self.width() / 2), self.height()))

        # Attributes
        self.players = []
        self.connection_manager = Websocket_connection_manager()
        self.connection_manager.run()

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)

        # Bottom frame
        control_frame = QtWidgets.QFrame()
        self.layout.addWidget(control_frame)
        control_layout = QtWidgets.QHBoxLayout()
        control_frame.setLayout(control_layout)

        # Add player button
        add_player_button = QtWidgets.QPushButton()
        add_player_button.setText("Add player")
        control_layout.addWidget(add_player_button)
        add_player_button.clicked.connect(self.add_player)

        # Reset players button
        reset_players_button = QtWidgets.QPushButton()
        reset_players_button.setText("Reset")
        control_layout.addWidget(reset_players_button)
        reset_players_button.clicked.connect(self.reset_players)

        # Github button
        github_button = QtWidgets.QPushButton(" App")
        github_button.setMaximumWidth(44)
        github_button.setToolTip("Link to the github page of the app")
        github_button.setStyleSheet("border: 0")
        github_button.clicked.connect(
            partial(webbrowser.open,
                    "https://github.com/FluffyMaguro/mini-casting-tool"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(HF.inner("src/github.png")),
                       QtGui.QIcon.Selected, QtGui.QIcon.On)
        github_button.setIcon(icon)
        control_layout.addWidget(github_button)

        # Maguro button
        maguro_button = QtWidgets.QPushButton(" Website")
        maguro_button.setMaximumWidth(60)
        maguro_button.setToolTip("Link to my website")
        maguro_button.setStyleSheet("border: 0")
        maguro_button.clicked.connect(
            partial(webbrowser.open, "https://www.maguro.one/"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(HF.inner("src/maguro.jpg")),
                       QtGui.QIcon.Selected, QtGui.QIcon.On)
        maguro_button.setIcon(icon)
        control_layout.addWidget(maguro_button)

        # Players
        players_frame = QtWidgets.QFrame(self)
        self.layout.addWidget(players_frame)
        self.player_layout = QtWidgets.QVBoxLayout()
        self.player_layout.setAlignment(QtCore.Qt.AlignTop)
        players_frame.setLayout(self.player_layout)
        self.add_player()
        self.add_player()

    def add_player(self):
        player_index = len(self.players)
        self.players.append(Player(player_index))
        self.player_layout.addWidget(self.players[-1])
        self.players[-1].btn_remove.clicked.connect(
            partial(self.remove_player, self.players[-1]))
        self.players[-1].data_changed.connect(self.player_data_changed)
        self.player_data_changed()

    def reset_players(self):
        for player in self.players:
            player.reset_player()
        self.player_data_changed()

    def remove_player(self, player_frame):
        self.player_layout.removeWidget(player_frame)
        self.players.remove(player_frame)
        player_frame.deleteLater()
        self.resize(self.width(), self.layout.sizeHint().height())
        self.player_data_changed()

    def player_data_changed(self):
        data = []
        for player in self.players:
            data.append(player.get_data())
        self.connection_manager.send(data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = AppWindow()
    MainWindow.show()
    sys.exit(app.exec_())
