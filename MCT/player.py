from functools import partial

from PyQt5 import QtCore, QtWidgets

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

        # Score
        self.score = QtWidgets.QLineEdit()
        self.score.setPlaceholderText("–")
        self.score.setToolTip("Player score. Don't change if best of one.")
        self.score.setMaximumWidth(30)
        self.score.setAlignment(QtCore.Qt.AlignCenter)
        self.score.textChanged.connect(self.data_changed.emit)
        layout.addWidget(self.score)

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
        self.bg_combo_box = QtWidgets.QComboBox()
        self.bg_combo_box.setToolTip("Change player background image")
        layout.addWidget(self.bg_combo_box)

        self.factions, self.backgrounds = HF.get_factions_backgrounds()

        for bg in self.backgrounds:
            self.bg_combo_box.addItem(bg)
        for f in self.factions:
            self.faction_combo_box.addItem(f)

        self.bg_combo_box.currentIndexChanged.connect(self.data_changed.emit)
        self.faction_combo_box.currentIndexChanged.connect(
            self.data_changed.emit)

        # Remove button
        self.btn_remove = QtWidgets.QPushButton()
        self.btn_remove.setToolTip("Remove player")
        self.btn_remove.setMaximumWidth(26)
        self.btn_remove.setStyleSheet("border :0px")
        self.btn_remove.setIcon(self.style().standardIcon(
            getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        layout.addWidget(self.btn_remove)

    def open_color_dialog(self, button):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            button.setStyleSheet(f'background-color: {color.name()}')
            self.data_changed.emit()

    def get_name(self):
        return self.player_name.text()

    def get_score(self):
        return self.score.text()

    def get_color(self):
        return self.color

    def get_faction(self):
        text = self.faction_combo_box.currentText()
        return self.factions[text]

    def get_background(self):
        text = self.bg_combo_box.currentText()
        return self.backgrounds[text]

    def get_data(self):
        """ Returns all player data"""
        return {
            'name': self.get_name(),
            'score': self.get_score(),
            'color': self.get_color(),
            'faction': self.get_faction(),
            'background': self.get_background()
        }
