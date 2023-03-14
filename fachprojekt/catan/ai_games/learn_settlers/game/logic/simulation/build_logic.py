import numpy as np, copy

from ai_games.learn_settlers.game.logic.helper_logic import HelperLogic
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.build_action import BuildCornerAction, BuildEdgeAction, RoadChangeAction
from ai_games.learn_settlers.game.objects.actions.phase_action import GamePhase
from ai_games.learn_settlers.game.objects.board import Corner
from ai_games.learn_settlers.game.objects.building import Building, BuildingType
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats

class SimBuildLogic:
    def __init__(self) -> None:
        pass

    @staticmethod
    def apply_longest_road(old_game_state:GameState, action:RoadChangeAction):
        game_state = copy.copy(old_game_state)
        game_state.players = copy.copy(game_state.players)
        if action.no_old != -1:
            player = copy.copy(game_state.players[action.no_old])
            player.victory_points -= 2
            player.longest_road = False
            game_state.players[action.no_old] = player
        if action.no_new != -1:
            player = copy.copy(game_state.players[action.no_new])
            player.victory_points += 2
            player.longest_road = True
            game_state.players[action.no_new] = player
        return game_state

    @classmethod
    def build_corner(cls, original_game_state:GameState, action:BuildCornerAction) -> GameState:
        game_state = copy.copy(original_game_state)
        players = copy.copy(game_state.players)
        game_state.players = players
        player = copy.copy(players[action.player_no])
        players[action.player_no] = player
        board = copy.copy(game_state.board)
        game_state.board = board
        corners = copy.copy(board.corners)
        board.corners = corners
        corner = copy.copy(corners[action.corner.id])
        corners[action.corner.id] = corner
        building = copy.copy(corner.building)
        corner.building = building
        player_buildings = copy.copy(player.buildings)
        player.buildings = player_buildings
        if action.building_type == BuildingType.SETTLEMENT:
            if not action.free:
                res_change = np.array([1,1,1,1,0,4])
                player.resources = player.resources - res_change
                game_state.resources = game_state.resources + res_change
            player.victory_points += 1
            player.settlement_count +=1
            building.build(action.player_no, BuildingType.SETTLEMENT) 
            player_buildings.append(corner.id)
            HelperLogic.update_possible_settlements(game_state, corner)
            if building.building_id == BuildingType.HARBOR_SETTLEMENT:
                assert building.resources is not None
                player.trade_costs = np.minimum(player.trade_costs, building.resources)
        elif action.building_type == BuildingType.CITY:
            if not action.free:
                res_change = np.array([0,0,0,2,3,5])
                player.resources = player.resources - res_change
                game_state.resources = game_state.resources + res_change
            player.victory_points += 1
            player.city_count +=1
            player.settlement_count -=1
            building.build(action.player_no, BuildingType.CITY)
        return game_state


    @classmethod
    def build_edge(cls, original_game_state:GameState, action:BuildEdgeAction) -> GameState:
        game_state = copy.copy(original_game_state)
        players = copy.copy(game_state.players)
        game_state.players = players
        player= copy.copy(players[action.player_no])
        players[action.player_no] = player
        player_roads = copy.copy(player.roads)
        player.roads = player_roads
        board = copy.copy(game_state.board)
        game_state.board = board
        edges = copy.copy(board.edges)
        board.edges = edges
        edge = copy.copy(edges[action.edge.id])
        edges[action.edge.id] = edge
        building = copy.copy(edge.building)
        edge.building = building

        if not action.free:
            res_change = np.array([1,1,0,0,0,2])
            player.resources = player.resources - res_change
            game_state.resources = game_state.resources + res_change
        elif game_state.phase != GamePhase.SETUP:
            game_state.road_building -= 1
            assert game_state.road_building >= 0
        assert action.building_type == BuildingType.ROAD
        building.build(action.player_no, BuildingType.ROAD)
        player_roads.append(edge.id)
        return game_state