import numpy as np, copy

from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.build_action import BuildCornerAction, BuildEdgeAction, RoadChangeAction
from ai_games.learn_settlers.game.objects.board import Corner
from ai_games.learn_settlers.game.objects.building import Building, BuildingType
from ai_games.learn_settlers.game.objects.game_state import GamePhase, GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats
from ai_games.learn_settlers.game.logic.helper_logic import HelperLogic

class BuildLogic:
    def __init__(self) -> None:
        pass

    @staticmethod
    def apply_longest_road(game_state:GameState, action:RoadChangeAction):
        if action.no_old != -1:
            player = game_state.players[action.no_old]
            player.victory_points -= 2
            player.longest_road = False
        if action.no_new != -1:
            player = game_state.players[action.no_new]
            player.victory_points += 2
            player.longest_road = True

    @classmethod
    def build_corner(cls, game_state:GameState, action:BuildCornerAction):
        player = game_state.players[action.player_no]
        corner = game_state.board.corners[action.corner.id]
        if action.building_type == BuildingType.SETTLEMENT:
            if not action.free:
                player.resources[0:4]-=1
                player.resources[-1]-=4
                game_state.resources[0:4]+=1
                game_state.resources[-1]+=4
            player.victory_points += 1
            player.settlement_count +=1
            corner.building.build(action.player_no, BuildingType.SETTLEMENT) 
            player.buildings.append(corner.id)
            HelperLogic.update_possible_settlements(game_state, corner)
            if corner.building.building_id == BuildingType.HARBOR_SETTLEMENT:
                assert corner.building.resources is not None
                player.trade_costs = np.minimum(player.trade_costs, corner.building.resources)
        elif action.building_type == BuildingType.CITY:
            if not action.free:
                player.resources[3]-=2
                player.resources[4]-=3
                player.resources[-1]-=5
                game_state.resources[3]+=2
                game_state.resources[4]+=3
                game_state.resources[-1]+=5
            player.victory_points += 1
            player.city_count +=1
            player.settlement_count -=1
            corner.building.build(action.player_no, BuildingType.CITY)

    @classmethod
    def build_edge(cls, game_state:GameState, action:BuildEdgeAction):
        player = game_state.players[action.player_no]
        if not action.free:
            player.resources[0:2]-=1
            player.resources[-1]-=2
            game_state.resources[0:2]+=1
            game_state.resources[-1]+=2
        elif game_state.phase != GamePhase.SETUP:
            game_state.road_building -= 1
            assert game_state.road_building >= 0
        assert action.building_type == BuildingType.ROAD
        edge = game_state.board.edges[action.edge.id]
        edge.building.build(action.player_no, BuildingType.ROAD)
        player.roads.append(edge.id)