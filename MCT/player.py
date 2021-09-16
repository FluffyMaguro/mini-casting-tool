from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

import MCT.helper_functions as HF


class Player(QtWidgets.QFrame):
    data_changed = QtCore.pyqtSignal()

    def __init__(self, index):
        super().__init__()

        self.color = HF.get_basic_color(index)
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.setMaximumHeight(38)

        # Name
        self.player_name = QtWidgets.QLineEdit()
        self.player_name.setPlaceholderText("Player name")
        self.player_name.setMaximumWidth(200)
        self.player_name.textChanged.connect(self.data_changed.emit)
        layout.addWidget(self.player_name)

        # Color
        color_button = QtWidgets.QPushButton()
        color_button.setToolTip("Change player color")
        color_button.setMaximumWidth(26)
        color_button.setStyleSheet(f'background-color: {self.color}')
        layout.addWidget(color_button)
        color_button.clicked.connect(
            partial(self.open_color_dialog, color_button))

        # Faction & background
        self.faction_combo_box = QtWidgets.QComboBox()
        self.faction_combo_box.setToolTip("Change player faction image")
        layout.addWidget(self.faction_combo_box)
        self.factions = HF.get_faction_images()

        for f in self.factions:
            self.faction_combo_box.addItem(f)

        self.faction_combo_box.currentIndexChanged.connect(
            self.data_changed.emit)

        # Score
        self.score = QtWidgets.QLineEdit()
        self.score.setPlaceholderText("–")
        self.score.setToolTip("Player score. Don't change if best of one.")
        self.score.setMaximumWidth(30)
        self.score.setAlignment(QtCore.Qt.AlignCenter)
        self.score.textChanged.connect(self.data_changed.emit)
        layout.addWidget(self.score)

        # Team
        self.team = QtWidgets.QLineEdit()
        self.team.setPlaceholderText("–")
        self.team.setToolTip("Player team. Don't change if best of one.")
        self.team.setMaximumWidth(30)
        self.team.setAlignment(QtCore.Qt.AlignCenter)
        self.team.textChanged.connect(self.data_changed.emit)
        layout.addWidget(self.team)

        # Remove button
        self.btn_remove = QtWidgets.QPushButton()
        self.btn_remove.setToolTip("Remove player")
        self.btn_remove.setMaximumWidth(26)
        self.btn_remove.setStyleSheet("border :0px")
        self.btn_remove.setIcon(self.style().standardIcon(
            getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        layout.addWidget(self.btn_remove)

    def reset_player(self, disconnect=True):
        """ Reset player name and score
        `disconnect` temporarily disconnect signals."""
        if disconnect:
            self.player_name.disconnect()
            self.score.disconnect()

        self.player_name.setText("")
        self.score.setText("")

        if disconnect:
            self.player_name.textChanged.connect(self.data_changed.emit)
            self.score.textChanged.connect(self.data_changed.emit)

    def open_color_dialog(self, button):
        color_dialog = QtWidgets.QColorDialog(self)
        color_dialog.setCurrentColor(QtGui.QColor(self.color))
        color_dialog.exec_()

        if not color_dialog.currentColor().isValid():
            return

        color = color_dialog.currentColor().name()
        if color != self.color:
            self.color = color
            button.setStyleSheet(f'background-color: {color}')
            self.data_changed.emit()

    def get_faction(self):
        text = self.faction_combo_box.currentText()
        return self.factions[text]

    def get_name(self):
        return self.player_name.text()

    def get_color(self):
        return self.color

    def get_score(self):
        return self.score.text()

    def get_team(self):
        return self.team.text()

    def get_data(self):
        """ Returns all player data"""
        return {
            'name': self.get_name(),
            'score': self.get_score(),
            'color': self.get_color(),
            'faction': self.get_faction(),
            'team': self.get_team()
        }
