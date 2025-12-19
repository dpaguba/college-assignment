from typing import Any
from ai_games.learn_settlers.com import *

from ai_games.learn_settlers.com.message_type import MessageType
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType
from ai_games.learn_settlers.game.objects.actions.build_action import BuildCornerAction, BuildEdgeAction
from ai_games.learn_settlers.game.objects.actions.card_action import CardAction
from ai_games.learn_settlers.game.objects.actions.dice_action import DiceAction
from ai_games.learn_settlers.game.objects.actions.discard_action import DiscardAction
from ai_games.learn_settlers.game.objects.actions.phase_action import PhaseAction
from ai_games.learn_settlers.game.objects.actions import RoadChangeAction
from ai_games.learn_settlers.game.objects.actions.robber_action import RobberAction
from ai_games.learn_settlers.game.objects.actions.trade_action import TradeAction
from ai_games.learn_settlers.game.objects.board import Board
from ai_games.learn_settlers.game.objects.board_objects import Corner, Edge, Tile
from ai_games.learn_settlers.game.objects.building import Building, BuildingType
from ai_games.learn_settlers.game.objects.game_state import GamePhase, GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats

class MessageEncoder():

    @staticmethod
    def encode_game_state(game_state:GameState) -> MyMessage:
        message = MyMessage()
        message.game_state.game_id = game_state.game_id
        message.game_state.phase = game_state.phase
        message.game_state.turn = game_state.turn
        message.game_state.last_roll = game_state.last_roll
        # Board
        for row in game_state.board.tiles:
            tile_list = TileList()
            for tile in row:
                mt = TileMessage()
                if tile is None:
                    mt.terrain = TerrainMessage.NONE
                else:
                    mt.r = tile.pos.r
                    mt.q = tile.pos.q
                    mt.terrain = tile.terrain
                    mt.dice = tile.dice
                tile_list.tiles.append(mt)
            message.game_state.board.tiles.append(tile_list)
        for harbor in game_state.board.harbors:
            em = EdgeMessage()
            em.id = harbor.id
            for t in harbor.tiles:
                tid = TileIdMessage()
                tid.r = t[0]
                tid.q = t[1]
                em.tiles.append(tid)
            em.building.player_no = harbor.building.player_no
            em.building.building_type = harbor.building.building_id
            if harbor.building.resources is not None:
                em.building.resources.extend(harbor.building.resources)
            message.game_state.board.harbors.append(em)
        for corner in game_state.board.corners:
            cm = CornerMessage()
            cm.id = corner.id
            for t in corner.tiles:
                tid = TileIdMessage()
                tid.r = t[0]
                tid.q = t[1]
                cm.tiles.append(tid)
            cm.building.player_no = corner.building.player_no
            cm.building.building_type = corner.building.building_id
            if corner.building.resources is not None:
                cm.building.resources.extend(corner.building.resources)
            message.game_state.board.corners.append(cm)
        for edge in game_state.board.edges:
            em = EdgeMessage()
            em.id = edge.id
            for t in edge.tiles:
                tid = TileIdMessage()
                tid.r = t[0]
                tid.q = t[1]
                em.tiles.append(tid)
            em.building.player_no = edge.building.player_no
            em.building.building_type = edge.building.building_id
            if edge.building.resources is not None:
                em.building.resources.extend(edge.building.resources)
            message.game_state.board.edges.append(em)
        # PlayerStats
        for player in game_state.players:
            pm = PlayerStatsMessage()
            pm.player_name = player.player_name
            pm.victory_points = player.victory_points
            pm.resources.extend(player.resources)
            pm.development_cards.extend(player.development_cards)
            pm.blocked_dev_cards.extend(player.blocked_dev_cards)
            pm.buildings.extend(player.buildings)
            pm.settlement_count = player.settlement_count
            pm.city_count = player.city_count
            pm.roads.extend(player.roads)
            pm.trade_costs.extend(player.trade_costs)
            pm.knights = player.knights
            pm.longest_road = player.longest_road
            pm.largest_army = player.largest_army
            pm.dev_card_played = player.dev_card_played
            message.game_state.players.append(pm)
        message.game_state.res_mult = game_state.res_mult
        for r in game_state.resources:
            message.game_state.resources.append(r)
        return message

    @classmethod
    def encode_build_corner_action(cls,message, action:BuildCornerAction) -> Message:
        message.player_no = action.player_no
        message.build_corner.corner.id = action.corner.id
        message.build_corner.corner.tiles.extend([TileIdMessage(r=x[0],q=x[1]) for x in action.corner.tiles])
        message.build_corner.corner.building.player_no = action.corner.building.player_no
        message.build_corner.corner.building.building_type = action.corner.building.building_id
        if action.corner.building.resources is not None:
            message.build_corner.corner.building.resources.extend(action.corner.building.resources)
        message.build_corner.building_type = action.building_type
        message.build_corner.free = action.free
        return message
    
    @classmethod
    def encode_build_edge_action(cls,message, action:BuildEdgeAction) -> Message:
        message.player_no = action.player_no
        message.build_edge.edge.id = action.edge.id
        message.build_edge.edge.tiles.extend([TileIdMessage(r=x[0],q=x[1]) for x in action.edge.tiles])
        message.build_edge.edge.building.player_no = action.edge.building.player_no
        message.build_edge.edge.building.building_type = action.edge.building.building_id
        if action.edge.building.resources is not None:
            message.build_edge.edge.building.resources.extend(action.edge.building.resources)
        message.build_edge.building_type = action.building_type
        message.build_edge.free = action.free
        return message
    
    @classmethod
    def encode_dice_action(cls, message, dice_action:DiceAction) -> Message:
        message.player_no = dice_action.player_no
        message.dice_action.dice_value = dice_action.dice_value
        return message
    
    @classmethod
    def encode_phase_change(cls, message, phase_action:PhaseAction) -> Message:
        message.player_no = phase_action.player_no
        message.phase_action.game_phase = phase_action.game_phase
        if phase_action.vp_update is not None:
            message.phase_action.vp_update.extend(phase_action.vp_update)
        return message
    
    @classmethod
    def encode_robber_action(cls, message, robber_action:RobberAction) -> Message:
        message.player_no = robber_action.player_no
        message.robber_action.tile.r = robber_action.tile.pos.r
        message.robber_action.tile.q = robber_action.tile.pos.q
        message.robber_action.tile.terrain = robber_action.tile.terrain
        message.robber_action.tile.dice = robber_action.tile.dice
        message.robber_action.target_player = robber_action.target_player
        message.robber_action.robber_type = robber_action.robber_type
        return message
    
    @classmethod
    def encode_trade_action(cls, message, trade_action:TradeAction)-> Message:
        message.player_no = trade_action.player_no
        message.trade_action.target_player = trade_action.target_player
        message.trade_action.out_resources.extend(trade_action.out_resources)
        message.trade_action.in_resources.extend(trade_action.in_resources)
        return message

    @classmethod
    def encode_card_action(cls, message, card_action:CardAction) -> Message:
        message.player_no = card_action.player_no
        message.card_action.draw = card_action.draw
        if card_action.card_type is not None:
            message.card_action.card_type = card_action.card_type
        else:
            message.card_action.card_type = -1
        return message
    
    @classmethod
    def encode_pass_action(cls, message, pass_action:Action) -> Message:
        message.player_no = pass_action.player_no
        message.pass_action = True
        return message
    
    @classmethod
    def encode_decline_action(cls, message, decline_action:Action) -> Message:
        message.player_no = decline_action.player_no
        message.decline_action = True
        return message
    
    @classmethod
    def encode_road_change_action(cls, message, action:RoadChangeAction) -> Message:
        message.player_no = action.player_no
        message.road_change.no_old = action.no_old
        message.road_change.no_new = action.no_new
        return message
    
    @classmethod
    def encode_discard_action(cls, message, action:DiscardAction) -> Message:
        message.player_no = action.player_no
        message.discard_action.discard_count = action.discard_count
        message.discard_action.out_resources.extend(action.out_resources)
        return message
    
    @classmethod
    def encode_action(cls, message, action:Action)-> Message:
            assert isinstance(action,Action)
            if action.action_type == ActionType.PASS:
                return cls.encode_pass_action(message, action)
            if action.action_type == ActionType.DECLINE:
                return cls.encode_decline_action(message, action)
            if isinstance(action,BuildCornerAction):
                return cls.encode_build_corner_action(message, action)
            if isinstance(action,BuildEdgeAction):
                return cls.encode_build_edge_action(message, action)
            if isinstance(action,DiceAction):
                return cls.encode_dice_action(message, action)
            if isinstance(action,PhaseAction):
                return cls.encode_phase_change(message, action)
            if isinstance(action,RobberAction):
                return cls.encode_robber_action(message, action)
            if isinstance(action,TradeAction):
                return cls.encode_trade_action(message, action)
            if isinstance(action,CardAction):
                return cls.encode_card_action(message, action)
            if isinstance(action,RoadChangeAction):
                return cls.encode_road_change_action(message, action)
            if isinstance(action, DiscardAction):
                return cls.encode_discard_action(message, action)
            raise NotImplementedError(f"Message type {action} not implemented")

    @classmethod
    def encode(cls, message_type:MessageType, payload:Action|GameState|list[Action]) -> MyMessage:
        match message_type:
            case MessageType.ACTIONLIST:
                assert isinstance(payload,list)
                message = MyMessage()
                message.action_request.actions.extend([cls.encode_action(ActionMessage(), x) for x in payload])
                return message
            case MessageType.ACTION:
                assert isinstance(payload,Action)
                message = MyMessage()
                cls.encode_action(message.action, payload)
                return message
            case MessageType.GAMESTATE:
                assert isinstance(payload,GameState)
                return cls.encode_game_state(payload)
            case _:
                raise NotImplementedError(f"Message type {message_type} not implemented")
