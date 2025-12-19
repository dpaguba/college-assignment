import queue, asyncio
import threading
import time
from typing import Any, Callable
import sys
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import QPushButton

from ai_games.learn_settlers.com import MessageType, Message
from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType
from ai_games.learn_settlers.game.objects.actions.card_action import CardAction
from ai_games.learn_settlers.game.objects.actions.dice_action import DiceAction
from ai_games.learn_settlers.game.objects.actions.phase_action import PhaseAction
from ai_games.learn_settlers.game.objects.actions.robber_action import RobberAction
from ai_games.learn_settlers.game.objects.actions.trade_action import TradeAction
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.game.player.player import Player, PlayerType


class UIPlayer(Player,QThread):
    update_signal = Signal()
    init_signal = Signal()

    def __init__(self, name:str = "", player_no: int = -1, substitute_player:Player|None = None, autoplay:bool = False) -> None:
        from PySide6.QtWidgets import QApplication, QMainWindow
        from ai_games.learn_settlers.ui.display import Display
        super().__init__(PlayerType.HUMAN, name=name)
        self.lock = threading.Lock()
        self.app = QApplication([])
        self.display = Display(self)
        self.message_type:MessageType|None = None
        self.possible_actions:list[Action] = []
        self.response = queue.Queue()
        self.changes = queue.Queue()
        self.trade = queue.Queue()
        self.autoplay = autoplay

        if substitute_player is not None:
            substitute_player.player_no = player_no
            substitute_player.client_id = self.client_id
        self.substitute_player = substitute_player


    @Slot()
    def handle_request_sub(self):
        if self.substitute_player is not None and self.message_type is not None:
            self.response.put(self.substitute_player.handle_request(self.message_type, self.possible_actions))
        
    @Slot()
    def handle_finish_game(self):
        self.autoplay = True
        if self.substitute_player is not None and self.message_type is not None:
            self.response.put(self.substitute_player.handle_request(self.message_type, self.possible_actions))


    def handle_request(self, message_type: MessageType, possible_actions: list[Action]):
        self.task = type
        self.possible_actions = possible_actions
        self.message_type = message_type
        # for action in self.possible_actions:
        #     print(action)
        self.update_signal.emit()
        # Debug autocomplete
        if self.substitute_player and self.autoplay:
            return self.substitute_player.handle_request(message_type, possible_actions)
        response =  self.response.get(True)
        return response
    
    def apply_action(self, action:Action):
        self.possible_actions = []
        # print(f"My action: {action}")
        # Check for validity
        self.response.put(action)

    def update_game_state(self, message_type: MessageType, action:Action|GameState):
        self.lock.acquire()
        super().update_game_state(message_type, action)
        if isinstance(action, GameState):
            self.init()
            self.update_signal.emit()
            self.lock.release()
            return
        assert isinstance(action,Action)
        self.changes.put(action)
        if isinstance(action,TradeAction) or isinstance(action,CardAction) or isinstance(action,RobberAction) or isinstance(action, PhaseAction) or isinstance(action, DiceAction) or  action.action_type== ActionType.DECLINE:
            self.trade.put(f"{str(action)}")
        self.update_signal.emit()
        self.lock.release()

    def init(self):
        self.init_signal.emit()

    def start_ui(self):
        self.display.show()
        sys.exit(self.app.exec())

    def set_game_state(self, game_state:GameState|None):
        super().set_game_state(game_state)
        if self.substitute_player:
            self.substitute_player.set_game_state(game_state)
        
    def prepare_game(self, action: PhaseAction):
        super().prepare_game(action)
        if self.substitute_player:
                self.substitute_player.prepare_game(action)

    def get_game_state(self):
        assert self.game_state is not None
        return self.game_state