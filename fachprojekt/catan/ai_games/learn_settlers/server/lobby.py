import logging.config, itertools
from concurrent.futures import ThreadPoolExecutor
import threading
from typing import Any, Optional
import typing

from ai_games.learn_settlers.com import *
from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.objects.game_state import GamePhase, GameState
from ai_games.learn_settlers.game.player.network_player import NetworkPlayer
from ai_games.learn_settlers.game.player.player import Player
from ai_games.learn_settlers.server.matchmaker.matchmaker import Matchmaker
from ai_games.learn_settlers.server.server import Server



# Logging
logging.config.fileConfig('ai_games/learn_settlers/utils/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
class Lobby:
    def __init__(self, hostname, port, matchmaker: Matchmaker, log_results = True) -> None:

        # Game
        self.log_results = log_results
        self.players:dict[str, NetworkPlayer] = {}
        self.matchmaker = matchmaker

        # Server
        self.server = Server(hostname, port, self.incoming_message_handler)
    
    def start_server(self):
        logger.debug("Start server")
        # self.executor.submit(self.server.start)
        self.server.start()

    def notify_player(self, client_id: str, message: Message):
        self.server.send(client_id, message)

    def notify_players(self, match: LearnSettlers, message: Message):
        logger.debug("Notifying players of match " + str(match.game_id) +" with " + str(message))
        for p in match.players:
            self.server.send(p.client_id, message)      
    
    def player_join(self, msg:MyMessage):
        client_id = msg.client_id
        player_type = msg.player_type
        player_name = msg.player_name
        try:
            player = self.players[client_id]
        except KeyError:
            player = NetworkPlayer(self.notify_player, player_type, client_id, player_name)
            self.players[client_id] = player
        self.matchmaker.player_join(player,msg.game_id)

    def start_game(self, msg:MyMessage):
        match_id = msg.game_id
        logger.info("Starting match: " + str(match_id))
        self.matchmaker.start_game(match_id)

    def incoming_message_handler(self, msg: MyMessage):
        if msg.HasField("hello"):
            return
        if msg.HasField("join"):
            self.player_join(msg.join)
            return
        if msg.HasField("start_game"):
            self.start_game(msg.start_game)
            return
        if msg.HasField("close"):
            return
        if msg.HasField("action"):
            self.players[msg.client_id].apply_action(msg)
            return

        logger.error("unknown Message: " + str(msg))
        