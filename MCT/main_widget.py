from functools import partial

from PyQt5 import QtCore, QtWidgets

from MCT.player import Player
from MCT.websocket import Websocket_connection_manager


class MainWidget(QtWidgets.QWidget):
    """ Main widget controlling players """
    def __init__(self):
        super().__init__()

        # Attributes
        self.players = []
        self.connection_manager = Websocket_connection_manager()
        self.connection_manager.run()
        self.connection_locked = False

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)

        # Control frame
        control_frame = QtWidgets.QFrame()
        self.layout.addWidget(control_frame)
        control_layout = QtWidgets.QHBoxLayout()
        control_layout.setContentsMargins(17, 0, 0, 0)
        control_frame.setLayout(control_layout)

        # Add player button
        add_player_button = QtWidgets.QPushButton()
        add_player_button.setText("Add player")
        add_player_button.setStatusTip("Add new player")
        add_player_button.clicked.connect(self.add_player)
        control_layout.addWidget(add_player_button)

        # Reset players button
        reset_players_button = QtWidgets.QPushButton()
        reset_players_button.setText("Reset")
        reset_players_button.setStatusTip("Resets players names and scores")
        reset_players_button.clicked.connect(self.reset_players)
        control_layout.addWidget(reset_players_button)

        # Text inbetween
        self.text_inbetween = QtWidgets.QLineEdit()
        self.text_inbetween.setPlaceholderText("Text between teams")
        self.text_inbetween.setStatusTip(
            'Text between players (for example "Best of 3")')
        self.text_inbetween.setMaximumWidth(200)
        self.text_inbetween.textChanged.connect(self.player_data_changed)
        control_layout.addWidget(self.text_inbetween)

        # Show score
        self.show_score = QtWidgets.QCheckBox("Show score")
        self.show_score.setMaximumWidth(100)
        self.show_score.setChecked(True)
        self.show_score.setStatusTip("Score can be hidden if none is set")
        self.show_score.stateChanged.connect(self.player_data_changed)
        control_layout.addWidget(self.show_score)

        # Players
        players_frame = QtWidgets.QFrame(self)
        self.layout.addWidget(players_frame)
        self.player_layout = QtWidgets.QVBoxLayout()
        self.player_layout.setAlignment(QtCore.Qt.AlignTop)
        players_frame.setLayout(self.player_layout)
        self.add_player()
        self.add_player()

    def add_player(self):
        self.players.append(Player(len(self.players)))
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
        self.parent().resize(self.parent().width(),
                             self.parent().layout().sizeHint().height())
        self.player_data_changed()

    def update_show_screen_checkbox(self):
        """ Check whether to show score based on checkbox and score values. Disable checkbox accordingly."""
        if any(i.get_score() for i in self.players):
            self.show_score.setChecked(True)
            self.show_score.setDisabled(True)
        else:
            self.show_score.setDisabled(False)

    def sync_player_scores(self):
        """ Disables and syncs player score widgets for additional players on the same team"""
        team_scores = dict()
        for player in self.players:
            team = player.get_team()
            if team in team_scores:
                player.score.setDisabled(True)
                player.score.setCurrentIndex(team_scores[team])
            else:
                team_scores[team] = player.get_score()
                player.score.setDisabled(False)

    def sort_players(self):
        """ Sort players based on their teams"""
        teams = [p.get_team() for p in self.players]
        for i in range(len(self.players)):
            if i == 0:
                continue
            # If the next player is in a lower team, find him a new place
            if teams[i] < teams[i - 1]:
                for new_place, team_iter in enumerate(teams):
                    if teams[i] < team_iter:
                        self.move_player(i, new_place)
                        # Start anew since we changed the player order
                        self.sort_players()
                        return

    def move_player(self, player_index, new_index):
        """ Moves a player to the new index. Updates self.players and layouts """
        player = self.players[player_index]
        self.players.remove(player)
        self.players.insert(new_index, player)
        self.player_layout.removeWidget(player)
        self.player_layout.insertWidget(new_index, player)

    def player_data_changed(self):
        """ What happens when player data is changed"""
        # This lock prevents this function from triggering itself again by changing data
        if self.connection_locked:
            return
        self.connection_locked = True

        self.sort_players()
        self.sync_player_scores()
        self.update_show_screen_checkbox()

        # Gather all data and send through a websocket
        data = [p.get_data() for p in self.players]
        self.connection_manager.send({
            "player_data": data,
            "text": self.text_inbetween.text(),
            "show_score": self.show_score.isChecked()
        })

        self.connection_locked = False
