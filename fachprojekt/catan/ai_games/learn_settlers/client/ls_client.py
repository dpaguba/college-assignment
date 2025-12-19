import logging.config
import random
import threading
import time

from ai_games.learn_settlers.client.client import Client
from ai_games.learn_settlers.com import *
from ai_games.learn_settlers.com.message_decoder import MessageDecoder
from ai_games.learn_settlers.com.message_encoder import MessageEncoder
from ai_games.learn_settlers.game.logic.direct.build_logic import BuildLogic
from ai_games.learn_settlers.game.logic.direct.card_logic import CardLogic
from ai_games.learn_settlers.game.logic.direct.trade_logic import TradeLogic
from ai_games.learn_settlers.game.logic.direct.turn_logic import TurnLogic
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.build_action import BuildCornerAction, BuildEdgeAction
from ai_games.learn_settlers.game.objects.actions.card_action import CardAction
from ai_games.learn_settlers.game.objects.actions.dice_action import DiceAction
from ai_games.learn_settlers.game.objects.actions.phase_action import PhaseAction
from ai_games.learn_settlers.game.objects.actions import RoadChangeAction
from ai_games.learn_settlers.game.objects.actions.robber_action import RobberAction
from ai_games.learn_settlers.game.objects.actions.trade_action import TradeAction
from ai_games.learn_settlers.game.objects.game_state import GamePhase, GameState
from ai_games.learn_settlers.game.player.player import Player

from ai_games.learn_settlers.com import *


logging.config.fileConfig('ai_games/learn_settlers/utils/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
class LSClient:
    def __init__(self, player:Player, verbose = False) -> None:
        self.finished = threading.Event()
        self.joined = threading.Event()
        self.client = Client(self.message_handler, client_id=player.client_id)
        self.player = player
        self.game_id:int = -1
        self.lock = threading.Lock()
        self.verbose = verbose


    def connect(self, uri):
        self.client.connect(uri)

    def close(self):
        self.client.close()

    # Make async? -> no active waiting
    def close_when_finished(self):
        self.finished.wait()
        self.close()

    def join_game(self,  game_id:int|None):
        msg = MyMessage()
        if game_id is not None:
            msg.join.game_id = game_id
        msg.join.client_id = self.player.client_id
        msg.join.player_type = self.player.player_type.value
        msg.join.player_name = self.player.player_name
        self.client.send_message(msg)

    def start_game(self, game_id = None):
        logger.debug("Starting Game")
        if game_id is None:
            self.joined.wait()
            game_id = self.game_id
        msg = MyMessage()
        msg.start_game.game_id = game_id
        msg.start_game.client_id = self.client.id
        self.client.send_message(msg)

    def reset_game(self):
        self.game_id = -1
        self.player.set_game_state(None)

    def apply_action(self, action):
        msg = MessageEncoder.encode(MessageType.ACTION, action)
        msg.client_id = self.client.id
        msg.game_id = self.game_id
        self.client.send_message(msg)

    def update_game_state(self, message_type:MessageType, action:Action|GameState):
        if isinstance(action, GameState):
            self.player.set_game_state(action)
            return
        game_state = self.player.get_game_state()
        if isinstance(action, BuildCornerAction):
            BuildLogic.build_corner(game_state, action)
            return
        elif isinstance(action, BuildEdgeAction):
            BuildLogic.build_edge(game_state,  action)
            return
        elif isinstance(action, DiceAction):
            TurnLogic.apply_dice(game_state, action)
            return
        elif isinstance(action, PhaseAction):
            # Game starts, we need to prepare the player
            if action.game_phase == GamePhase.WAITING:
                self.player.prepare_game(action)
            TurnLogic.phase_change(game_state, action)
            return
        elif isinstance(action, TradeAction):
            TradeLogic.apply_trade(game_state, action)
            return
        elif isinstance(action, RobberAction):
            TurnLogic.handle_robber_action(game_state, action)
            return
        elif isinstance(action, CardAction):
            if action.draw:
                CardLogic.add_card(game_state, action)
                return 
            else:
                CardLogic.play_card(game_state, action)
                return
        elif isinstance(action, RoadChangeAction):
            BuildLogic.apply_longest_road(game_state, action)
            return
        raise NotImplementedError


    def message_handler(self, msg: MyMessage):
        self.lock.acquire()
        if msg.HasField("welcome"):
            self.player.client_id = self.client.id
            logger.info("Connected with ID: " + str(self.client.id))
            self.lock.release()
            return
        if msg.HasField("join"):
            if self.client.id == msg.join.client_id:
                self.game_id =msg.join.game_id
                print(f"Joined Game {self.game_id}")
                self.joined.set()
            self.lock.release()
            return
        if msg.HasField("close"):
            self.finished.set()
            self.lock.release()
            return
        message_type, action = MessageDecoder.decode(msg)
        if isinstance(action, list):
            try:
                action = self.player.handle_request(message_type, action)
            except Exception as e:
                # select random action
                action = action[random.randint(0, len(action)-1)]
            self.apply_action(action)
            self.lock.release()
            return
        self.update_game_state(message_type, action)
        if self.verbose and message_type == MessageType.GAMESTATE:
            print(f"Game Started {time.strftime('%H:%M:%S')}")
        if isinstance(action, PhaseAction):
            assert self.player.game_state is not None
            if self.verbose and action.game_phase == GamePhase.ENDED:
                print(f"Game Ended {time.strftime('%H:%M:%S')}")
                # for player in self.player.game_state.players:
                #     print(f"{player.player_name} has {player.victory_points} Points")
        self.lock.release()
        return