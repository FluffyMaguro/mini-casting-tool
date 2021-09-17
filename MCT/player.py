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
        self.player_name.setStatusTip("Change player name")
        self.player_name.setMaximumWidth(200)
        self.player_name.textChanged.connect(self.data_changed.emit)
        layout.addWidget(self.player_name)

        # Color
        color_button = QtWidgets.QPushButton()
        color_button.setStatusTip("Change player color")
        color_button.setMaximumWidth(26)
        color_button.setStyleSheet(f'background-color: {self.color}')
        layout.addWidget(color_button)
        color_button.clicked.connect(
            partial(self.open_color_dialog, color_button))

        # Faction & background
        self.faction_combo_box = QtWidgets.QComboBox()
        self.faction_combo_box.setStatusTip("Change player faction image")
        layout.addWidget(self.faction_combo_box)
        self.factions = HF.get_faction_images()
        for f in self.factions:
            self.faction_combo_box.addItem(f)
        self.faction_combo_box.currentIndexChanged.connect(
            self.data_changed.emit)

        # Team
        self.team = QtWidgets.QComboBox()
        self.team.setMaximumWidth(70)
        for i in range(1, 16):
            self.team.addItem(f"Team {i:02}")
        self.team.setCurrentIndex(index)
        self.team.setStatusTip("Change player team")
        self.team.currentIndexChanged.connect(self.data_changed.emit)
        layout.addWidget(self.team)

        # Score
        self.score = QtWidgets.QComboBox()
        self.score.setMaximumWidth(72)
        for i in range(0, 16):
            self.score.addItem(f"Score: {i}")
        self.score.setStatusTip("Change player score")
        self.score.currentIndexChanged.connect(self.data_changed.emit)
        layout.addWidget(self.score)

        # Remove button
        self.btn_remove = QtWidgets.QPushButton()
        self.btn_remove.setStatusTip("Remove player")
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
        self.score.setCurrentIndex(0)

        if disconnect:
            self.player_name.textChanged.connect(self.data_changed.emit)
            self.score.currentIndexChanged.connect(self.data_changed.emit)

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
        return self.score.currentIndex()

    def get_team(self):
        return self.team.currentIndex() + 1

    def get_data(self):
        """ Returns all player data"""
        return {
            'name': self.get_name(),
            'score': self.get_score(),
            'color': self.get_color(),
            'faction': self.get_faction(),
            'team': self.get_team()
        }
