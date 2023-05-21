import copy
import uuid

from ai_games.learn_settlers.com import *

from ai_games.learn_settlers.com.message_decoder import MessageDecoder
from ai_games.learn_settlers.com.message_encoder import MessageEncoder
from ai_games.learn_settlers.com.message_type import MessageType
from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.board import Board
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.utils.game_state_compare import GameStateCompare
from ai_games.learn_settlers.utils.log_reader import LogReader


class MessageTester():
    def __init__(self, id:int, size:int, no_players:int):
        self.game = LearnSettlers(id,size)
        players = [RandomPlayer(f"Player{i}") for i in range(no_players)]
        for p in players:
            self.game.add_player(p)
        self.game.add_callback(self.test)
        self.remote_game_state = copy.deepcopy(self.game.game_state)
        self.action_log = []
        self.message_log = []

    def run_test(self):
        self.game.run()
        
        

    def test(self, message_type:MessageType, action:Action):
        message = MessageEncoder.encode(message_type, action)

        message_string = message.SerializeToString()
        self.action_log.append(action)
        self.message_log.append(message_string)

        new_message = MyMessage()
        new_message.ParseFromString(message_string)

        backup = copy.deepcopy(self.remote_game_state)

        new_remote_game_state = MessageDecoder.apply_message( new_message, self.remote_game_state)
        assert GameStateCompare.compare_gamestates(self.game.game_state,new_remote_game_state)
        assert GameStateCompare.compare_gamestates(backup,self.remote_game_state)
        self.remote_game_state = new_remote_game_state
        