# This Python file uses the following encoding: utf-8
import random
import typing

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtCore import Slot, QBasicMutex, Qt
from PySide6.QtGui import QColor, QBrush,QMouseEvent, QPainter
import numpy as np

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ai_games.learn_settlers.game.objects.actions import *
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.ui.board_view import GraphicCorner, GraphicEdge, GraphicTile
from ai_games.learn_settlers.ui.legacy_board_widget import BoardWidget
from ai_games.learn_settlers.ui.ui_player import UIPlayer
from ai_games.learn_settlers.ui.ui_form import Ui_Display

class Display(QMainWindow):
    def __init__(self, player: UIPlayer, parent=None):
        super().__init__(parent)
        self.player = player
        self.ui = Ui_Display()
        self.ui.setupUi(self)
        self.lock = QBasicMutex()
        self._connect_signals()

    def init(self):
        # legacy board for comparison
        assert self.player.game_state
        # self.ui.board_ui.set_board(self.player.game_state)
        self.ui.board.set_board(self.player.game_state)
        self._set_resources()
        self._set_dev_cards()
        self._set_trade()

    def update_log(self, text):
        self.ui.log.append(text)

    def _set_resources(self):
        assert self.player.game_state
        self.ui.dice_button.setText(str(f"{self.player.game_state.last_roll}"))
        self.ui.resources.setColumnCount(9)
        self.ui.resources.setRowCount(len(self.player.game_state.players)+1)
        self.ui.resources.setHorizontalHeaderLabels([ "Wood", "Brick", "Sheep", "Wheat", "Ore", "Sum", "Dev", "KP", "VP"])
        self.ui.resources.setVerticalHeaderLabels([player.player_name for player in self.player.game_state.players]+["Bank"])
        for i in range(len(self.player.game_state.players)):
            self.ui.resources.verticalHeaderItem(i).setBackground(QBrush(QColor(BoardWidget.PLAYER_COLORS[i])))
        for i, player in enumerate(self.player.game_state.players):
            for j in range(0,6):
                self.ui.resources.setItem(i, j, QTableWidgetItem(str(player.resources[j])))
            self.ui.resources.setItem(i, 6, QTableWidgetItem(str(player.development_cards[-1])))
            self.ui.resources.setItem(i, 7, QTableWidgetItem(str(player.knights)))
            self.ui.resources.setItem(i, 8, QTableWidgetItem(str(player.victory_points)))
        for j in range(0,6):
            self.ui.resources.setItem(len(self.player.game_state.players), j, QTableWidgetItem(str(self.player.game_state.resources[j])))
        
    def _set_dev_cards(self):
        assert self.player.game_state
        self.ui.dev_cards.setColumnCount(6)
        self.ui.dev_cards.setHorizontalHeaderLabels(["Knights", "Roads", "YoP", "Monopoly","VPs", "Sum(Buy)"])
        my_player = self.player.game_state.players[self.player.player_no]
        for i in range(6):
            self.ui.dev_cards.setItem(0, i, QTableWidgetItem(str(my_player.development_cards[i])))

    def _set_trade(self):
        self.ui.trade_values.setColumnCount(6)
        self.ui.trade_values.setRowCount(2)
        self.ui.trade_values.setHorizontalHeaderLabels(["player_no", "Wood", "Brick", "Sheep", "Wheat", "Ore"])
        self.ui.trade_values.setVerticalHeaderLabels(["Mine", "Other"])
        self.ui.trade_values.setItem(0, 0, QTableWidgetItem(str(self.player.player_no)))
        item = QTableWidgetItem(str(self.player.player_no))
        # remove to add cheating options
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.ui.trade_values.setItem(0, 0, item)
        item = QTableWidgetItem(str(-1))
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.ui.trade_values.setItem(1, 0, item)
        for i in range (0,2):
            item = QTableWidgetItem(str(self.player.player_no))
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.ui.trade_values.setItem(i, 0, item)
            for j in range(1,6):
                item = QTableWidgetItem("0")
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.ui.trade_values.setItem(i,j,item)

    def _connect_signals(self):
        self.ui.end_turn_button.clicked.connect(self.end_turn)
        self.ui.dice_button.clicked.connect(self.dice_action)
        self.ui.trade_button.clicked.connect(self.trade_action)
        self.ui.decline_button.clicked.connect(self.decline)
        self.ui.discard_button.clicked.connect(self.discard_action)
        self.ui.dev_cards.horizontalHeader().sectionClicked.connect(self.card_action)
        self.ui.ai_turn_button.clicked.connect(self.player.handle_request_sub)
        self.ui.end_match_button.clicked.connect(self.player.handle_finish_game)
        # self.ui.board_ui.mouseReleaseEvent = self.click_on_board
        self.ui.board.mousePressEvent = self.board_action
        self.player.update_signal.connect(self.game_update)
        self.player.init_signal.connect(self.init)

    @typing.no_type_check
    def update_resources(self):
        assert self.player.game_state
        self.ui.dice_button.setText(str(f"{self.player.game_state.last_roll}"))
        for i, player in enumerate(self.player.game_state.players):
            for j in range(0,6):
                self.ui.resources.item(i, j).setText(str(player.resources[j]))
            self.ui.resources.item(i, 6).setText(str(player.development_cards[-1]))
            self.ui.resources.item(i, 7).setText(str(player.knights))
            self.ui.resources.item(i, 8).setText(str(player.victory_points))
        for j in range(0,6):
            self.ui.resources.item(len(self.player.game_state.players), j).setText(str(self.player.game_state.resources[j]))
        my_player = self.player.game_state.players[self.player.player_no]
        for i in range(6):
            self.ui.dev_cards.item(0, i).setText(str(my_player.development_cards[i]))

    def request(self):
        self.ui.status.setText("Your Turn")
        self.ui.pos_action_list.setText("")
        for action in self.player.possible_actions:
                self.ui.pos_action_list.append(str(action))

    def response(self, action:Action):
        self.ui.status.setText("Waiting for Game")
        self.ui.pos_action_list.setText("")
        if len(self.player.possible_actions) > 0:
            self.player.apply_action(action)

    def game_update(self):
        assert self.player.game_state
        self.lock.lock()
        # self.ui.board_ui.set_board(self.player.game_state)
        # Update resources based on actions
        self.update_resources()
        while not self.player.changes.empty():
            action = self.player.changes.get_nowait()
            if isinstance(action, GameState):
                self.ui.board.set_board(action)
                continue
            assert isinstance(action, Action)
            if isinstance(action, BuildCornerAction) or isinstance(action, BuildEdgeAction):
                self.ui.board.update_board(action)
                continue
            if isinstance(action, DiceAction):
                # TODO
                continue
            if isinstance(action, TradeAction):
                # TODO
                continue
            if isinstance(action, CardAction):
                # TODO
                continue
            if isinstance(action, PhaseAction):
                # TODO
                continue
            if isinstance(action,RobberAction):
                self.ui.board.update_robber(action)
                # Handle non board updates
                continue
            if isinstance(action, RoadChangeAction):
                continue
            if action.action_type == ActionType.PASS:
                continue
            if action.action_type == ActionType.DECLINE:
                continue
            if isinstance(action, DiscardAction):
                continue
            print(action)
            raise NotImplementedError
        while not self.player.trade.empty():
            self.update_log(self.player.trade.get())
        if len(self.player.possible_actions) > 0:
            self.request()
        self.lock.unlock()


    # def click_on_board (self, event:QMouseEvent):
    #     self.ui.board_ui.clicked = (event.x(), event.y())
    #     self.ui.board_ui.update()
    #     print("Click on board")
    #     x,y = self.ui.board_ui.pixel_to_hex(event.x(), event.y())
    #     print(f"{x} {y}")
        


    @Slot()
    def end_turn(self):
        action = Action(self.player.player_no)
        if action in self.player.possible_actions:
            self.response(Action(self.player.player_no))
            
    @Slot()
    def decline(self):
        action = Action(self.player.player_no, ActionType.DECLINE)
        if action in self.player.possible_actions:
            self.response(Action(self.player.player_no))

    @Slot()
    def dice_action(self):
        dice_actions = [x for x in self.player.possible_actions if x.action_type == ActionType.DICE]
        if len(dice_actions)>0:
            self.response(dice_actions[0])

    @typing.no_type_check
    @Slot()
    def trade_action(self):
        if len(self.player.possible_actions)>0:
            my_no = int(self.ui.trade_values.item(0,0).text())
            my_values = np.array([int(self.ui.trade_values.item(0,i).text()) for i in range(1,6)]+[0], dtype=int)
            my_values[-1] = my_values[0:-1].sum()
            other_no = int(self.ui.trade_values.item(1,0).text())
            other_values = np.array([int(self.ui.trade_values.item(1,i).text()) for i in range(1,6)]+[0],dtype=int)
            other_values[-1] = other_values[0:-1].sum()
            action = TradeAction(my_no,other_no,my_values,other_values)
            self.response(action)
        else:
            print("Trading only during the turn")
    
    @Slot()
    def discard_action(self):
        res_to_discard = np.array([int(self.ui.trade_values.item(0,i).text()) for i in range(1,6)]+[0], dtype=int)
        res_to_discard[-1] = res_to_discard[0:-1].sum()
        if res_to_discard[-1] < 0:
            res_to_discard *= -1
        action = DiscardAction(
            self.player.player_no, 
            res_to_discard[-1],
            res_to_discard
        )
        self.response(action)

    def board_action(self, event:QMouseEvent):
        assert self.player.game_state is not None
        item = self.ui.board.itemAt(event.pos())
        while (parent:=item.parentItem()) is not None:
            item = parent
        if isinstance(item, GraphicTile):
            # Robber action
            robber_actions = [x for x in self.player.possible_actions if isinstance(x, RobberAction) and x.robber_type == RobberActionType.PLACE]
            if len(robber_actions) ==0:
                return
            tile = self.player.game_state.board.get_tile_by_id(item.id)
            assert tile is not None
            action = RobberAction(self.player.player_no, RobberActionType.PLACE,tile,-1)
        elif isinstance(item, GraphicEdge):
            # Build Road
            edge = self.player.game_state.board.edges[item.id]
            edge_actions = [x for x in self.player.possible_actions if isinstance(x, BuildEdgeAction) and x.edge == edge]
            if len(edge_actions) == 0:
                return
            action = edge_actions[0]
        elif isinstance(item, GraphicCorner):
            # Build Settlement, City or steal when there was a robber placed
            corner = self.player.game_state.board.corners[item.id]
            if isinstance(self.player.possible_actions[-1], RobberAction):
                # deal with robber
                target_id =  corner.building.player_no
                robber_actions = [x for x in self.player.possible_actions if isinstance(x, RobberAction) and x.target_player == target_id]
                if len(robber_actions) == 0:
                    return
                action = robber_actions[0]
            else:
                corner_actions = [x for x in self.player.possible_actions if isinstance(x, BuildCornerAction) and x.corner == corner]
                if len(corner_actions) == 0:
                    return
                assert len(corner_actions) == 1
                action = corner_actions[0]
        else:
            print(f"unkown Item: {item}")
            return
        self.response(action)

    @Slot() # type: ignore
    def card_action(self,index):
        if index == 5:
            action = CardAction(self.player.player_no,True)
        else:
            action = CardAction(self.player.player_no,False,DevelopmentCard(index))
        self.response(action)

    @Slot()
    def random_action(self):
        self.ui.status.setText("Waiting")
        try:
            self.player.apply_action(self.player.possible_actions[random.randint(0, len(self.player.possible_actions)-1)])
        except IndexError:
            self.ui.status.setText("No possible actions")