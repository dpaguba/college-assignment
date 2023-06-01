import copy
from enum import IntEnum
from typing import Any
import uuid

from PySide6.QtCore import QThread

from ai_games.learn_settlers.com.message_type import MessageType
from ai_games.learn_settlers.game.objects.actions import *
from ai_games.learn_settlers.game.objects.actions.phase_action import PhaseAction
from ai_games.learn_settlers.game.objects.game_state import GamePhase, GameState

class PlayerType(IntEnum):
    AI = 0
    HUMAN = 1

# Abstract class for players
class Player(QThread):
    def __init__(self, player_type:PlayerType, name:str = "") -> None:
        super().__init__(None)
        self.player_name = name
        self.client_id:str = uuid.uuid4().hex
        self.player_no = -1
        self.player_type = player_type
        self.game_state:GameState |None = None
        # Players might be reused in multiple matches.
        # Any initialization that is match specific should be done when a new game is prepared

    def handle_request(self, message_type: MessageType, possible_actions: list[Action])-> Action:
        raise NotImplementedError
    
    # Handle game state updates, mostly important for network players
    def update_game_state(self, message_type:MessageType, action:Action|GameState):
        # local player game state updates are handled by the game itself
        if isinstance(action, GameState):
            self.set_game_state(action)
            return
        if isinstance(action, PhaseAction):
            self.prepare_game(action)
            return

    def set_game_state(self, game_state:GameState|None):
        self.game_state = game_state
        
    def prepare_game(self, action:PhaseAction):
        if action.game_phase == GamePhase.WAITING:
            # A new game begins. We might need our player number
            self.player_no = action.player_no
        return
    
    def get_game_state(self):
        assert self.game_state is not None
        return self.game_state
