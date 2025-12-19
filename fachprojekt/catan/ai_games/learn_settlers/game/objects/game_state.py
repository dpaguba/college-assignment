from enum import IntEnum
import typing, logging.config
import numpy as np

from ai_games.learn_settlers.game.objects.actions.phase_action import GamePhase
from ai_games.learn_settlers.game.objects.board import Board, Tile
from ai_games.learn_settlers.game.objects.board_objects import Pos
from ai_games.learn_settlers.game.objects.card_deck import CardDeck
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats

from ai_games.learn_settlers.com import *
from ai_games.learn_settlers.game.objects.resource import Resource
from ai_games.learn_settlers.game.objects.terrain import Terrain


class RobberState(IntEnum):
    NO_STATE = 0
    PLACE_ROBBER = 1
    STEAL_RESOURCE = 2

logging.config.fileConfig('ai_games/learn_settlers/utils/logging.ini', disable_existing_loggers=False)
class GameState:
    def __init__(self, game_id:int, board_size:int, board = None, players = None, resources:list[int]|None = None, res_mult:int = 19, turn = 0, last_roll = -1, robber_tile:Tile|None = None, phase = GamePhase.WAITING) -> None:
        self.game_id = game_id
        self.phase = phase
        self.turn = turn
        self.current_player = 0
        self.current_turn_moves = 0
        self.discarding:list[int] = []
        self.robber_state = RobberState.NO_STATE
        self.monopoly = False
        self.year_of_plenty = 0
        self.road_building = 0
        self.trade_ongoing = False
        # TODO track played cards
        self.last_roll = last_roll
        if board is None:
            board = Board.generate_board(board_size,"random")
        self.board:Board = board
        if players is None:
            players = []
        self.players:list[PlayerStats] = players
        self.res_mult = res_mult
        if resources is None:
            resources = [res_mult for _ in Resource]
            resources[-1]*= 5
        self.resources = np.array(resources)
        if robber_tile is None:
            robber_tile = [x for r in self.board.tiles for x in r if x is not None and x.terrain == Terrain.Desert][0]
        self.robber_tile:Pos = robber_tile.pos

    def check_integrity(self) -> bool:
        if self.resources[0:5].sum() != self.resources[5]:
            logging.error("Resources are not equal")
            print("Resources are not equal")
            return False
        if not all(self.resources >= 0):
            logging.error("a Resource is negative")
            print("a Resource is negative")
            return False
        for player in self.players:
            if player.resources[0:5].sum() != player.resources[5]:
                logging.error(f"Player Resources are not equal for {player.player_name}")
                print(f"Player Resources are not equal for {player.player_name}")
                return False
            if not all(player.resources >= 0):
                logging.error("a Player Resource is negative")
                print("a Player Resource is negative")
                return False
        return True
