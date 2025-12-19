import random
import threading, logging.config
from typing import Callable
import numpy as np
from ai_games.learn_settlers.com.message_type import MessageType
from ai_games.learn_settlers.game.logic.direct.build_logic import BuildLogic
from ai_games.learn_settlers.game.logic.direct.card_logic import CardLogic
from ai_games.learn_settlers.game.logic.game_logic import GameLogic
from ai_games.learn_settlers.game.logic.helper_logic import HelperLogic
from ai_games.learn_settlers.game.logic.direct.trade_logic import TradeLogic
from ai_games.learn_settlers.game.logic.direct.turn_logic import TurnLogic
from ai_games.learn_settlers.game.objects.actions.card_action import CardAction, DevelopmentCard
from ai_games.learn_settlers.game.objects.actions.dice_action import DiceAction
from ai_games.learn_settlers.game.objects.actions.phase_action import PhaseAction
from ai_games.learn_settlers.game.objects.actions.robber_action import RobberAction
from ai_games.learn_settlers.game.objects.actions.trade_action import TradeAction
from ai_games.learn_settlers.game.objects.card_deck import CardDeck
from ai_games.learn_settlers.game.objects.game_state import GamePhase, GameState, RobberState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats
from ai_games.learn_settlers.game.player.player import Player
from ai_games.learn_settlers.utils.game_log import GameLog
from ai_games.learn_settlers.game.objects.actions import *
from ai_games.learn_settlers.utils.game_state_compare import GameStateCompare

WIN_COUNT = 10

logging.config.fileConfig('ai_games/learn_settlers/utils/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
class LearnSettlers():
    def __init__(self, game_id:int, board_size:int, logging_enabled:bool = False) -> None:
        # self.lock = threading.Lock()
        self.game_id = game_id
        self.players:list[Player] = []
        self.board_size = board_size
        self.callback:list[Callable] = []
        self.current_player = 0
        self.game_log = GameLog(game_id, enabled = logging_enabled)
        if logging_enabled:
            self.add_callback(self.game_log.append)
        self.reset()

    def reset(self, keep_players=False):
        self.game_state = GameState(self.game_id, self.board_size)
        self.game_logic = GameLogic()
        if keep_players:
            self.game_state.players  = [PlayerStats(player.player_name) for player in self.players]
        else:
            self.players = []

    def add_player(self, player:Player):
        if self.game_state.phase != GamePhase.WAITING:
            return False
        player_no = len(self.players)
        player.player_no = player_no
        self.players.append(player)
        self.game_state.players.append(PlayerStats(player.player_name))
        return True
        # self.players_by_id[player.client_id] = player

    def add_callback(self, callback:Callable):
        self.callback.append(callback)

    def is_started(self):
        return self.game_state.phase != GamePhase.WAITING
    
    # Sends a message to all players and the logger to adjust their gamestates
    def handle_updates(self,message_type:MessageType, action:Action|GameState):
        # update to interested parties
        # logger.info(f"{action}")
        for player in self.players:
            player.update_game_state(message_type, action)
            # assert player.game_state is not None
            # GameStateCompare.compare_gamestates(self.game_state, player.game_state)
        for callback in self.callback:
            callback(message_type, action)
    
    def run(self):
        self.start_game()
        assert not any([p.player_no is None for p in self.players])
        
        while self.game_state.phase != GamePhase.ENDED:
            possible_actions = self.game_logic.get_possible_actions_main(self.game_state)
            player = self.players[possible_actions[0].player_no]
            action = player.handle_request(MessageType.ACTIONLIST, possible_actions)
            action, additional_work = self.game_logic.process_action(self.game_state, action)
            
            # TODO check discard actions
            GameLogic.apply_action(self.game_state, action)
            self.handle_updates(MessageType.ACTION, action)
            if action.action_type == ActionType.PASS and self.game_state.current_player == 0:
                logger.debug(f"Turn {self.game_state.turn}")
                logger.debug(f"{[p.victory_points for p in self.game_state.players]}")
            elif additional_work is not None:
                if isinstance(additional_work, RoadChangeAction):
                    GameLogic.apply_action(self.game_state, additional_work)
                    self.handle_updates(MessageType.ACTION, additional_work)
                elif isinstance(additional_work, RobberAction):
                    GameLogic.apply_action(self.game_state, additional_work)
                    self.handle_updates(MessageType.ACTION, additional_work)
                elif isinstance(action, TradeAction):
                    assert isinstance(additional_work,list)
                    if action.target_player == -2:
                        for a in additional_work:
                            GameLogic.apply_action(self.game_state, a)
                            self.handle_updates(MessageType.ACTION, a)
                    elif action.target_player >= 0:
                        assert additional_work[0].player_no != self.game_state.current_player
                        a = self.players[additional_work[0].player_no].handle_request(MessageType.ACTIONLIST, additional_work)
                        GameLogic.apply_action(self.game_state, a)
                        self.handle_updates(MessageType.ACTION, a)
        logger.info(f"Finished after Turn {self.game_state.turn}")
        logger.info([p.victory_points for p in self.game_state.players])
        self.game_log.write()
        return [int(p.victory_points) for p in self.game_state.players]
    
    # Sets everything up for a new game and notifys the players
    def start_game(self):
        self.handle_updates(MessageType.GAMESTATE, self.game_state)
        for i, player in enumerate(self.players):
            start_action = PhaseAction(i, GamePhase.WAITING, [])
            player.update_game_state(MessageType.ACTION, start_action)
        setup_phase = PhaseAction(0,game_phase=GamePhase.SETUP)
        GameLogic.apply_action(self.game_state, setup_phase)
        self.handle_updates(MessageType.ACTION, setup_phase)
    
    def finish_game(self, game_state:GameState):
        phase_change = PhaseAction(self.current_player, GamePhase.ENDED, [p.victory_points for p in game_state.players])
        self.handle_updates(MessageType.ACTION, phase_change)
        TurnLogic.phase_change(self.game_state, phase_change)
        logger.info(f"Finished after Turn {self.game_state.turn}")
        logger.info([p.victory_points for p in game_state.players])
        self.game_log.write()
        return [int(p.victory_points) for p in game_state.players]
    
    # Experimental:TODO check.
    def next(self, action:Action) -> list[Action]:
        action, additional_work = self.game_logic.process_action(self.game_state, action)
        
        # TODO check discard actions
        GameLogic.apply_action(self.game_state, action)
        self.handle_updates(MessageType.ACTION, action)
        if action.action_type == ActionType.PASS and self.game_state.current_player == 0:
            logger.debug(f"Turn {self.game_state.turn}")
            logger.debug(f"{[p.victory_points for p in self.game_state.players]}")
        elif additional_work is not None:
            if isinstance(additional_work, RoadChangeAction):
                GameLogic.apply_action(self.game_state, additional_work)
                self.handle_updates(MessageType.ACTION, additional_work)
            elif isinstance(additional_work, RobberAction):
                GameLogic.apply_action(self.game_state, additional_work)
                self.handle_updates(MessageType.ACTION, additional_work)
            elif isinstance(action, TradeAction):
                assert isinstance(additional_work,list)
                if action.target_player == -2:
                    for a in additional_work:
                        GameLogic.apply_action(self.game_state, a)
                        self.handle_updates(MessageType.ACTION, a)
                elif action.target_player >= 0:
                    assert additional_work[0].player_no != self.game_state.current_player
                    return additional_work
                    a = self.players[additional_work[0].player_no].handle_request(MessageType.ACTIONLIST, additional_work)
                    GameLogic.apply_action(self.game_state, a)
                    self.handle_updates(MessageType.ACTION, a)
        return self.game_logic.get_possible_actions_main(self.game_state)
    
    def run_stepwise(self):
        self.start_game()
        assert not any([p.player_no is None for p in self.players])
        possible_actions = self.game_logic.get_possible_actions_main(self.game_state)
        while self.game_state.phase != GamePhase.ENDED:
            player = self.players[possible_actions[0].player_no]
            action = player.handle_request(MessageType.ACTIONLIST, possible_actions)
            possible_actions = self.next(action)
            
        logger.info(f"Finished after Turn {self.game_state.turn}")
        logger.info([p.victory_points for p in self.game_state.players])
        self.game_log.write()
        return [int(p.victory_points) for p in self.game_state.players]