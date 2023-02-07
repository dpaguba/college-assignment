import numpy as np
from ai_games.learn_settlers.game.objects.actions import RoadChangeAction
from ai_games.learn_settlers.game.objects.board_objects import Corner
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats


class HelperLogic:
    
    @classmethod
    def dfs_longest_road(cls, game_state:GameState, player_no:int, corner:Corner, visited:set[Corner])->int:
        max_length = 0
        neighboring_roads = [r for r in game_state.board.get_neighbors_of_corner(corner.id) if r.building.player_no == player_no]
        for road in neighboring_roads:
            next_corner = [c for c in game_state.board.get_neighbors_of_edge(road.id) if c != corner][0] # always length 1
            if next_corner in visited or (corner.building.player_no != player_no and corner.building.player_no != -1):
                continue
            visited.add(next_corner)
            length = cls.dfs_longest_road(game_state, player_no, next_corner, visited)
            if length > max_length:
                max_length = length
            visited.remove(next_corner)
        return max_length + 1

    @classmethod
    def longest_road(cls, game_state:GameState, player_no:int) -> int:
        player = game_state.players[player_no]
        road_length = 0
        road_corners = set([c for r in player.roads for c in game_state.board.get_neighbors_of_edge(r) if c.building.player_no == player_no or c.building.player_no == -1])
        for rc in road_corners:
            visited = set()
            visited.add(rc)
            length = cls.dfs_longest_road(game_state, player_no, rc, visited)
            if length > road_length:
                road_length = length
        return road_length

    @classmethod
    def update_longest_road(cls,game_state:GameState, player_no:int) -> RoadChangeAction|None:
        road_length = np.array([cls.longest_road(game_state, i) for i in range(len(game_state.players))], dtype=int)
        prev_longest_road = [p.longest_road for p in game_state.players]
        max_length = road_length.max()
        if any(prev_longest_road):
            prev_longest_idx = np.argmax(prev_longest_road)
            if max_length < 5:
                return RoadChangeAction(player_no, int(prev_longest_idx), -1)
            longest_road = road_length == max_length
            if longest_road[prev_longest_idx]:
                return None
            if longest_road.sum() > 1:
                return RoadChangeAction(player_no, int(prev_longest_idx), -1)
            longest_road_idx = np.argmax(longest_road)
            return RoadChangeAction(player_no, int(prev_longest_idx), int(longest_road_idx))
        else:
            if max_length < 5:
                return None
            longest_road = road_length == max_length
            if sum(longest_road) > 1:
                # Happens if there are multiple players with the second longest road when the longest road is removed
                return None
            longest_road_idx = np.argmax(longest_road)
            return RoadChangeAction(player_no, -1, int(longest_road_idx))

    @classmethod
    def update_possible_settlements(cls, game_state:GameState, new_settlement:Corner):
        corners = [game_state.board.corners[y]  for x in new_settlement.tiles for y  in game_state.board.cornermap[x]]
        corners = [x for x in corners if new_settlement.diff(x) <= 1]
        game_state.board.possible_settlements = game_state.board.possible_settlements.difference(corners)

    @staticmethod
    def update_resources(game_state:GameState, player:PlayerStats, resources:np.ndarray):
        adj_resources = np.minimum(game_state.resources, resources)
        adj_resources[-1] = adj_resources[0:-1].sum()
        player.resources += adj_resources
        game_state.resources -= adj_resources
        
    @staticmethod
    def sim_update_resources(game_state:GameState, player:PlayerStats, resources:np.ndarray):
        adj_resources = np.minimum(game_state.resources, resources)
        adj_resources[-1] = adj_resources[0:-1].sum()
        player.resources = player.resources + adj_resources
        game_state.resources = game_state.resources - adj_resources
