import logging.config
import queue
import random
from typing import Any, Callable
from ai_games.learn_settlers.com import MessageType, Message
from ai_games.learn_settlers.com.message_decoder import MessageDecoder
from ai_games.learn_settlers.com.message_encoder import MessageEncoder
from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.game.player.player import Player, PlayerType

from ai_games.learn_settlers.com import *

# Player that relays all the information to a remote client.
logging.config.fileConfig('ai_games/learn_settlers/utils/logging.ini', disable_existing_loggers=False)
class NetworkPlayer(Player):
    def __init__(self, remote_callback:Callable, player_type:PlayerType, client_id:str, name:str = "") -> None:
        super().__init__(player_type, name=name)
        self.client_id = client_id
        self.remote_callback = remote_callback
        self.response = queue.Queue()
        self.possible_actions = []

    def msg_to_client(self, message:MyMessage):
        self.remote_callback(self.client_id, message)

    # Forward options to remote player
    def handle_request(self, message_type: MessageType, possible_actions: list[Action]):
        message = MessageEncoder.encode(message_type, possible_actions)
        self.response = queue.Queue()
        self.possible_actions = possible_actions
        self.msg_to_client(message)
        try:
            response = self.response.get(True, timeout=20)
        except queue.Empty:
            logging.error(f"No response from {self.player_name}: {self.client_id}")
            response = random.choice(self.possible_actions)
        return response
    
    # Forward Message from remote player to game
    def apply_action(self, msg: Action):
        msg_type, action = MessageDecoder.decode(msg)
        assert isinstance(action, Action)
        if not action in self.possible_actions:
            logging.info(f"Invalid action from {self.player_name}: {self.client_id}")
            # choose random action
            action = random.choice(self.possible_actions)
        self.response.put(action)
    
    # Forward game state updates to remote player
    def update_game_state(self, message_type:MessageType, action:Action|GameState):
        message = MessageEncoder.encode(message_type, action)
        self.remote_callback(self.client_id, message)
    