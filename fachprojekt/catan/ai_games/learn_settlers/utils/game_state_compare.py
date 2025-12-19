from ai_games.learn_settlers.game.objects.board import Board
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats


class GameStateCompare():
    @classmethod
    def compare_players(cls,player1:PlayerStats, player2:PlayerStats) ->  bool:
        if player1.player_name != player2.player_name:
            raise ValueError(f"Player Name mismatch: {player1.player_name} != {player2.player_name}")
        if player1.victory_points != player2.victory_points:
            raise ValueError(f"Victory Points mismatch: {player1.victory_points} != {player2.victory_points}")
        if any(player1.resources != player2.resources):
            raise ValueError(f"Resources mismatch: {player1.resources} != {player2.resources}")
        if any(player1.development_cards != player2.development_cards):
            raise ValueError(f"Development Cards mismatch: {player1.development_cards} != {player2.development_cards}")
        if player1.buildings != player2.buildings:
            raise ValueError(f"Buildings mismatch: {player1.buildings} != {player2.buildings}")
        if player1.settlement_count != player2.settlement_count:
            raise ValueError(f"Settlement Count mismatch: {player1.settlement_count} != {player2.settlement_count}")
        if player1.city_count != player2.city_count:
            raise ValueError(f"City Count mismatch: {player1.city_count} != {player2.city_count}")
        if player1.roads != player2.roads:
            raise ValueError(f"Roads mismatch: {player1.roads} != {player2.roads}")
        if any(player1.trade_costs != player2.trade_costs):
            raise ValueError(f"Trade Costs mismatch: {player1.trade_costs} != {player2.trade_costs}")
        if player1.knights != player2.knights:
            raise ValueError(f"Knights mismatch: {player1.knights} != {player2.knights}")
        if player1.longest_road != player2.longest_road:
            raise ValueError(f"Longest Road mismatch: {player1.longest_road} != {player2.longest_road}")
        if player1.largest_army != player2.largest_army:
            raise ValueError(f"Largest Army mismatch: {player1.largest_army} != {player2.largest_army}")
        return True

    @classmethod
    def compare_board(cls, board1:Board, board2:Board) -> bool:
        if board1.size != board2.size:
            raise ValueError(f"Board Size mismatch: {board1.size} != {board2.size}")
        if board1.offset != board2.offset:
            raise ValueError(f"Board Offset mismatch: {board1.offset} != {board2.offset}")
        for r1,r2 in zip(board1.tiles, board2.tiles):
            for t1,t2 in zip(r1,r2):
                if t1 is None and t2 is None:
                    continue
                if t1 is None or t2 is None:
                    raise ValueError(f"Tile mismatch: {t1} != {t2}")
                if t1.dice != t2.dice:
                    raise ValueError(f"Dice mismatch: {t1.dice} != {t2.dice}")
                if t1.pos != t2.pos:
                    raise ValueError(f"Position mismatch: {t1.pos} != {t2.pos}")
                if t1.terrain != t2.terrain:
                    raise ValueError(f"Terrain mismatch: {t1.terrain} != {t2.terrain}")
        for c1,c2 in zip(board1.corners, board2.corners):
            if c1.id != c2.id:
                raise ValueError(f"Corner ID mismatch: {c1.id} != {c2.id}")
            for t1,t2 in zip(c1.tiles, c2.tiles):
                if t1[0] != t2[0]:
                    raise ValueError(f"Tile mismatch: {t1[0]} != {t2[0]}")
                if t1[1] != t2[1]:
                    raise  ValueError(f"Tile mismatch: {t1[1]} != {t2[1]}")
            if c1.building.player_no != c2.building.player_no:
                raise ValueError(f"Player No mismatch: {c1.building.player_no} != {c2.building.player_no}")
            if c1.building.building_id != c2.building.building_id:
                raise ValueError(f"Building ID mismatch: {c1.building.building_id} != {c2.building.building_id}")
            if c1.building.resources is not None and c2.building.resources is not None:
                if any(c1.building.resources != c2.building.resources):
                    raise ValueError(f"Resources mismatch: {c1.building.resources} != {c2.building.resources}")
            if c1.building.resources is None and c2.building.resources is not  None:
                raise ValueError(f"Resources mismatch: {c1.building.resources} != {c2.building.resources}")
            elif c1.building.resources is not None and c2.building.resources is None:
                raise ValueError(f"Resources mismatch: {c1.building.resources} != {c2.building.resources}")
        for e1,e2 in zip(board1.edges, board2.edges):
            if e1.id != e2.id:
                raise ValueError(f"Edge ID mismatch: {e1.id} != {e2.id}")
            for t1,t2 in zip(e1.tiles, e2.tiles):
                if t1[0] != t2[0]:
                    raise ValueError(f"Tile mismatch: {t1[0]} != {t2[0]}")
                if t1[1] != t2[1]:
                    raise ValueError(f"Tile mismatch: {t1[1]} != {t2[1]}")
            if e1.building.player_no != e2.building.player_no:
                raise ValueError(f"Player No mismatch: {e1.building.player_no} != {e2.building.player_no}")
            if e1.building.building_id != e2.building.building_id:
                raise ValueError(f"Building ID mismatch: {e1.building.building_id} != {e2.building.building_id}")
            if e1.building.resources is not None and e2.building.resources is not None:
                if any(e1.building.resources != e2.building.resources):
                    raise ValueError(f"Resources mismatch: {e1.building.resources} != {e2.building.resources}")
            if e1.building.resources is None and e2.building.resources is not  None:
                raise ValueError(f"Resources mismatch: {e1.building.resources} != {e2.building.resources}")
            elif e1.building.resources is not None and e2.building.resources is None:
                raise ValueError(f"Resources mismatch: {e1.building.resources} != {e2.building.resources}")
        if len(board1.possible_settlements) != len(board2.possible_settlements):
            raise ValueError(f"Possible Settlement mismatch: {board1.possible_settlements} != {board2.possible_settlements}")
        for x in board1.possible_settlements:
            if x not in board2.possible_settlements:
                raise ValueError(f"Possible Settlement mismatch: {x} not in {board2.possible_settlements}")
        return True


    @classmethod
    def compare_gamestates(cls, original:GameState, other:GameState) -> bool:
        # False on divergence
        if original.game_id != other.game_id:
            raise ValueError(f"Game ID mismatch: {original.game_id} != {other.game_id}")
        if original.phase != other.phase:
            raise ValueError(f"Game Phase mismatch: {original.phase} != {other.phase}")
        if original.turn != other.turn:
            raise ValueError(f"Turn number mismatch: {original.turn} != {other.turn}")
        if original.current_player != other.current_player:
            raise ValueError(f"Current Player mismatch: {original.current_player} != {other.current_player}")
        if original.current_turn_moves !=other.current_turn_moves:
            raise ValueError("Move missmatch")
        if original.discarding != other.discarding:
            raise ValueError(f"Discarding mismatch: {original.discarding} != {other.discarding}")
        if original.robber_state != other.robber_state:
            raise ValueError(f"Robber ongoing mismatch: {original.robber_state} != {other.robber_state}")
        if original.monopoly != other.monopoly:
            raise ValueError(f"Trading mismatch: {original.monopoly} != {other.monopoly}")
        if original.year_of_plenty != other.year_of_plenty:
            raise ValueError(f"Year of Plenty mismatch: {original.year_of_plenty} != {other.year_of_plenty}")
        if original.road_building != other.road_building:
            raise ValueError(f"Road Building mismatch: {original.road_building} != {other.road_building}")
        if original.trade_ongoing != other.trade_ongoing:
            raise ValueError(f"Trade ongoing mismatch: {original.trade_ongoing} != {other.trade_ongoing}")
        if original.last_roll != other.last_roll:
            raise ValueError(f"Last Roll mismatch: {original.last_roll} != {other.last_roll}")
        if not cls.compare_board(original.board, other.board):
            raise ValueError("Board mismatch")
        for p1,p2 in zip(original.players, other.players):
            if not cls.compare_players(p1,p2):
                raise ValueError("Player mismatch")
        if original.res_mult != other.res_mult:
            raise ValueError(f"Resource Multiplier mismatch: {original.res_mult} != {other.res_mult}")
        if any(original.resources != other.resources):
            raise ValueError(f"Resources mismatch: {original.resources} != {other.resources}")
        # Dev Cards are secret, no need to compare
        if original.robber_tile != other.robber_tile:
            raise ValueError(f"Robber mismatch: {original.robber_tile} != {other.robber_tile}")
        return True