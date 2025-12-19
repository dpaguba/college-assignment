from typing import Any

import numpy as np
from ai_games.learn_settlers.com import *

from ai_games.learn_settlers.com.message_type import MessageType
from ai_games.learn_settlers.game.logic.game_logic import GameLogic
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType
from ai_games.learn_settlers.game.objects.actions.build_action import BuildCornerAction, BuildEdgeAction
from ai_games.learn_settlers.game.objects.actions.card_action import CardAction, DevelopmentCard
from ai_games.learn_settlers.game.objects.actions.dice_action import DiceAction
from ai_games.learn_settlers.game.objects.actions.discard_action import DiscardAction
from ai_games.learn_settlers.game.objects.actions.phase_action import PhaseAction
from ai_games.learn_settlers.game.objects.actions import RoadChangeAction
from ai_games.learn_settlers.game.objects.actions.robber_action import RobberAction, RobberActionType
from ai_games.learn_settlers.game.objects.actions.trade_action import TradeAction
from ai_games.learn_settlers.game.objects.board import Board
from ai_games.learn_settlers.game.objects.board_objects import Corner, Edge, Pos, Tile
from ai_games.learn_settlers.game.objects.building import Building, BuildingType
from ai_games.learn_settlers.game.objects.game_state import GamePhase, GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats
from ai_games.learn_settlers.game.objects.terrain import Terrain

class MessageDecoder():

    @classmethod
    def decode_building(cls, building:BuildingMessage) -> Building:
        resources = building.resources if len(building.resources) > 0 else None 
        return Building(building.player_no, BuildingType(building.building_type), resources)

    @classmethod
    def decode_corner(cls, corner:CornerMessage) -> Corner:
        tiles = corner.tiles
        building = cls.decode_building(corner.building)
        corner = Corner(corner.id, Pos(tiles[0].r, tiles[0].q),Pos(tiles[1].r, tiles[1].q),Pos(tiles[2].r, tiles[2].q), building)
        return corner
    
    @classmethod
    def decode_edge(cls, edge:EdgeMessage) -> Edge:
        tiles = edge.tiles
        building =  cls.decode_building(edge.building)
        edge = Edge(edge.id, Pos(tiles[0].r, tiles[0].q),Pos(tiles[1].r, tiles[1].q), building)
        return edge
    
    @classmethod
    def decode_tile(cls, tile:TileMessage) -> Tile|None:
        if tile.terrain == TerrainMessage.NONE:
            return None
        return Tile(tile.r, tile.q, Terrain(tile.terrain), tile.dice)

    @classmethod
    def decode_player_stats(cls, message:PlayerStatsMessage) -> PlayerStats:
        player_name = message.player_name
        victory_points = message.victory_points
        resources = message.resources
        development_cards = message.development_cards
        blocked_dev_cards = message.blocked_dev_cards
        buildings = [x for x in message.buildings]
        roads = [x for x in message.roads]
        knights = message.knights
        longest_road = message.longest_road
        largest_army = message.largest_army
        trade_costs = message.trade_costs
        settlement_count = message.settlement_count
        city_count = message.city_count
        dev_card_played = message.dev_card_played

        player = PlayerStats(player_name,victory_points,resources,development_cards, buildings, roads, knights, longest_road, largest_army, trade_costs, settlement_count, city_count, blocked_dev_cards, dev_card_played)
        return player
    
    @classmethod
    def decode_board(cls, message:BoardMessage) -> Board:
        tiles = [[cls.decode_tile(x) for x in y.tiles] for y in message.tiles]
        corners = [cls.decode_corner(x) for x in message.corners]
        edges = [cls.decode_edge(x) for x in message.edges]
        harbors = [cls.decode_edge(x) for x in message.harbors]
        board = Board(tiles,edges, corners, harbors)
        return board
        

    @classmethod
    def decode_game_state(cls, message:GameStateMessage)->GameState:
        game_id = message.game_id
        game_phase = GamePhase(message.phase)
        turn = message.turn
        last_roll = message.last_roll
        res_mult = message.res_mult
        board = cls.decode_board(message.board)
        players = [cls.decode_player_stats(x) for x in message.players]
        resources = message.resources
        robber = board.tiles[message.robber.r][message.robber.q]
        
        game_state = GameState(game_id, 0,board,players,resources,res_mult, turn, last_roll,robber, game_phase)
        return game_state

    @classmethod
    def decode_corner_action(cls, player_no, message:BuildCornerMessage) -> BuildCornerAction:
        corner = cls.decode_corner(message.corner)
        message.building_type
        return BuildCornerAction(player_no, corner, BuildingType(message.building_type),message.free)

    @classmethod
    def decode_edge_action(cls, player_no:int, message:BuildEdgeMessage) -> BuildEdgeAction:
        edge = cls.decode_edge(message.edge)
        return BuildEdgeAction(player_no, edge, BuildingType.ROAD, message.free)
    
    @classmethod
    def decode_dice_action(cls, player_no:int, message:DiceActionMessage) -> Action:
        return DiceAction(player_no, message.dice_value)
    
    @classmethod
    def decode_phase_action(cls, player_no:int, message:PhaseActionMessage) -> Action:
        if len(message.vp_update) > 0:
            return PhaseAction(player_no, GamePhase(message.game_phase), message.vp_update)
        return PhaseAction(player_no, GamePhase(message.game_phase))
    
    @classmethod
    def decode_trade_action(cls, player_no:int, message:TradeActionMessage) -> Action:
        return TradeAction(player_no, message.target_player, np.array(message.out_resources, dtype=int), np.array(message.in_resources, dtype=int))
    
    @classmethod
    def decode_robber_action(cls, player_no:int, message:RobberActionMessage) -> Action:
        tile = cls.decode_tile(message.tile)
        assert tile is not None
        return RobberAction(player_no, RobberActionType(message.robber_type), tile, message.target_player)
    
    @classmethod
    def decode_card_action(cls, player_no:int, message:CardActionMessage) -> Action:
        dev_card = DevelopmentCard(message.card_type) if  message.card_type >= 0 else None       
        return CardAction(player_no, message.draw,dev_card)

    @classmethod
    def decode_pass_action(cls, player_no:int, message:Message):
        return Action(player_no)
    
    @classmethod
    def decode_decline_action(cls, player_no:int, message:Message):
        return Action(player_no, ActionType.DECLINE)
    
    @classmethod
    def decode_road_change_action(cls, player_no:int, message:RoadChangeMessage) -> Action:
        return RoadChangeAction(player_no, message.no_old, message.no_new)
    
    @classmethod
    def decode_discard_action(cls, player_no:int, message:DiscardMessage) -> Action:
        return DiscardAction(player_no, message.discard_count,np.array(message.out_resources, dtype=int))

    @classmethod
    def decode_action(cls, message:ActionMessage):
        player_no = message.player_no
        if message.HasField("build_corner"):
            return cls.decode_corner_action(player_no, message.build_corner)
        if message.HasField("build_edge"):
            return cls.decode_edge_action(player_no, message.build_edge)
        if message.HasField("dice_action"):
            return cls.decode_dice_action(player_no, message.dice_action)
        if message.HasField("phase_action"):
            return cls.decode_phase_action(player_no, message.phase_action)
        if message.HasField("robber_action"):
            return cls.decode_robber_action(player_no, message.robber_action)
        if message.HasField("trade_action"):
            return cls.decode_trade_action(player_no, message.trade_action)
        if message.HasField("card_action"):
            return cls.decode_card_action(player_no, message.card_action)
        if message.HasField("pass_action"):
            return cls.decode_pass_action(player_no, message.pass_action)
        if message.HasField("road_change"):
            return cls.decode_road_change_action(player_no, message.road_change)
        if message.HasField("decline_action"):
            return cls.decode_decline_action(player_no, message.decline_action)
        if message.HasField("discard_action"):
            return cls.decode_discard_action(player_no, message.discard_action)
        raise NotImplementedError("Not implemented")

    @classmethod
    def decode(cls,message:MyMessage) -> tuple[MessageType,Action|GameState|list[Action]]:
        if message.HasField("game_state"):
            return MessageType.GAMESTATE, cls.decode_game_state(message.game_state)
        if message.HasField("action_request"):
            return MessageType.ACTIONLIST, [cls.decode_action(x) for x in message.action_request.actions]
        if message.HasField("action"):
            return MessageType.ACTION, cls.decode_action(message.action)
        raise NotImplementedError("Not implemented")

    @classmethod
    def apply_message(cls, message:Message, game_state:GameState|None = None) -> GameState:
        message_type, action = cls.decode(message)
        if message_type == MessageType.GAMESTATE:
            assert isinstance(action, GameState)
            return action
        assert isinstance(action, Action)
        assert game_state is not None
        return GameLogic.sim_apply_action(game_state, action)