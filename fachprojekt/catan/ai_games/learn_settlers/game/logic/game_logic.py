import copy
import numpy as np
from ai_games.learn_settlers.game.logic.direct.build_logic import BuildLogic
from ai_games.learn_settlers.game.logic.direct.card_logic import CardLogic
from ai_games.learn_settlers.game.logic.direct.turn_logic import TurnLogic
from ai_games.learn_settlers.game.logic.helper_logic import HelperLogic
from ai_games.learn_settlers.game.logic.simulation.build_logic import SimBuildLogic
from ai_games.learn_settlers.game.logic.simulation.card_logic import SimCardLogic
from ai_games.learn_settlers.game.logic.simulation.trade_logic import SimTradeLogic
from ai_games.learn_settlers.game.logic.simulation.turn_logic import SimTurnLogic
from ai_games.learn_settlers.game.logic.direct.trade_logic import TradeLogic
from ai_games.learn_settlers.game.objects.actions import *
from ai_games.learn_settlers.game.objects.building import BuildingType
from ai_games.learn_settlers.game.objects.card_deck import CardDeck
from ai_games.learn_settlers.game.objects.game_state import GamePhase, GameState, RobberState
from ai_games.learn_settlers.game.objects.terrain import Terrain


class GameLogic():
    
    def __init__(self, max_settlements = 5, max_cities = 4, max_roads = 15, win_count = 10, card_deck:list[DevelopmentCard] | None  = None):
        self.max_settlements = max_settlements
        self.max_cities = max_cities
        self.max_roads = max_roads
        self.win_count = win_count
        self.card_deck = CardDeck(card_deck)
        self.zeroes = np.zeros(6, dtype=int)
        self.monopoly = False
    
    def check_victory(self, game_state:GameState) -> bool:
        victory_points = [p.victory_points for p in game_state.players]
        if game_state.turn > 300:
            return True
        for i,p in enumerate(game_state.players):
            victory_points[i] += p.development_cards[DevelopmentCard.VICTORY_POINT]
        if any([vp >= self.win_count for vp in victory_points]):
            return True
        else:
            return False
    
    @staticmethod
    def get_possible_new_roads(game_state:GameState, player_no:int)-> list[Action]:
        player = game_state.players[player_no]
        roads = player.roads
        #adjacent_corners = [x for x in game_state.board.corners if any([x.diff(y)<=1 for y in settlements])]
        adjacent_corners = set([c for r in roads for c in game_state.board.get_neighbors_of_edge(r)])

        possible_roads = [r for c in adjacent_corners for r in game_state.board.get_neighbors_of_corner(c.id) if r.building.building_id == BuildingType.EMPTY]
        possible_road_actions:list[Action] =  [BuildEdgeAction(player_no, x, BuildingType.ROAD, True) for x in possible_roads]
        if len(possible_road_actions)==0:
            return [Action(player_no, ActionType.DECLINE)]
        return possible_road_actions

    def get_possible_build_actions(self, game_state:GameState)-> list[Action]:
        player_no = game_state.current_player
        player = game_state.players[player_no]
        settlements = player.buildings
        roads = player.roads
        #adjacent_corners = [x for x in game_state.board.corners if any([x.diff(y)<=1 for y in settlements])]
        adjacent_corners = set([c for r in roads for c in game_state.board.get_neighbors_of_edge(r)])

        possible_actions:list[Action] = []

        # Roads
        if all(player.resources[0:2]>0) and len(player.roads) < self.max_roads:
            possible_roads = [r for c in adjacent_corners for r in game_state.board.get_neighbors_of_corner(c.id) if r.building.building_id == BuildingType.EMPTY]
            possible_actions += [BuildEdgeAction(player_no, x, BuildingType.ROAD) for x in possible_roads]

        # Settlements
        if all(player.resources[0:4]>0) and player.settlement_count < self.max_settlements:
            possible_settlements = game_state.board.possible_settlements.intersection(adjacent_corners)
            possible_actions+= [BuildCornerAction(player_no, x, BuildingType.SETTLEMENT) for x in possible_settlements]

        # Cities
        if player.resources[3]>2 and  player.resources[4]>3 and player.city_count < self.max_cities:
            possible_cities = [c for x in settlements if (c:=game_state.board.corners[x]).building.building_id == BuildingType.SETTLEMENT or c.building.building_id == BuildingType.HARBOR_SETTLEMENT]
            possible_actions+= [BuildCornerAction(player_no, x, BuildingType.CITY) for x in possible_cities]
        

        return possible_actions

    @classmethod
    def get_setup_city_actions(cls, game_state:GameState, player_no:int) -> list[Action]:
        actions:list[Action] = [BuildCornerAction(player_no, x, BuildingType.SETTLEMENT, True) for x in game_state.board.possible_settlements]
        return actions

    @classmethod
    def get_setup_road_actions(cls, game_state:GameState, player_no:int)-> list[Action]:
        last_corner = game_state.board.corners[game_state.players[player_no].buildings[-1]]
        possible_edges = [x for x in game_state.board.get_neighbors_of_corner(last_corner.id) if x.building.building_id == BuildingType.EMPTY]
        actions:list[Action] = [BuildEdgeAction(player_no, x, BuildingType.ROAD, True) for x in possible_edges]
        return actions

    @classmethod
    def get_possible_trade_actions(cls, game_state:GameState) -> list[Action]:
        player = game_state.players[game_state.current_player]
        possible_trades:list[Action] = []
        for resource in range(5):
            # Base Trade
            if player.resources[resource] > player.trade_costs[resource]:
                out_res = np.zeros(6, dtype=int)
                out_res[resource] = player.trade_costs[resource]
                out_res[-1] = player.trade_costs[resource] - 1
                for i in range(5):
                    if i == resource or game_state.resources[i] <= 0:
                        continue
                    in_res = np.zeros(6, dtype=int)
                    in_res[i] = 1
                    possible_trades.append(TradeAction(game_state.current_player, -1,out_res,np.array(in_res)))
        return possible_trades

    @classmethod
    def get_possible_card_actions(cls, game_state:GameState, card_deck:CardDeck) -> list[Action]:
        player = game_state.players[game_state.current_player]
        actions:list[Action] = []
        if len(card_deck.stack)>0 and player.resources[2]>= 1 and player.resources[3] >= 1 and player.resources[4] >= 1:
            actions.append(CardAction(game_state.current_player, True))
        if not player.dev_card_played:
            for i in range(4):
                if player.development_cards[i] > 0:
                    actions.append(CardAction(game_state.current_player, False, DevelopmentCard(i)))
        return actions
    
    @classmethod
    def get_possible_robber_placement_actions(cls, game_state:GameState, player_no:int) -> list[Action]:
        return [RobberAction(player_no, RobberActionType.PLACE,tile)for row in game_state.board.tiles for tile in row if tile != game_state.robber_tile and not tile is None and tile.terrain != Terrain.Water]
    
    @classmethod
    def get_possible_robber_steal_actions(cls, game_state:GameState, player_no:int) -> list[Action]:
        tile = game_state.board.get_tile_by_id(game_state.robber_tile)
        assert tile is not None
        corners = game_state.board.cornermap[tile.pos]
        targets = {corner.building.player_no for corner_id in corners if (corner:=game_state.board.corners[corner_id]).building.player_no >= 0 and corner.building.player_no != player_no}
        res:list[Action] = [RobberAction(player_no, RobberActionType.STEAL, tile, target_player=target) for target in targets]
        if len(res) > 0:
            return res
        else:
            return[Action(player_no, ActionType.DECLINE)]
    
    @classmethod
    def get_year_of_plenty_actions(cls, game_state:GameState, player_no:int)-> list[Action]:
        actions: list[Action] = []
        for res in range(5):
            if game_state.resources[res] > 0:
                in_res = np.zeros(6, dtype=int)
                in_res[[res,-1]] = 1
                actions.append(TradeAction(player_no, -1, np.zeros(6, dtype=int), in_res))
        if len(actions) == 0:
            actions = [Action(player_no, ActionType.DECLINE)]
        return actions

    @classmethod
    def get_monopoly_actions(cls,game_state:GameState, player_no:int) -> list[Action]:
        actions: list[Action] = []
        gain = np.array([game_state.res_mult]*5)-game_state.resources[0:5]-game_state.players[player_no].resources[0:5]
        for res in range(5):
            if gain[res] > 0:
                in_res = np.zeros(6, dtype=int)
                in_res[[res,-1]] = gain[res]
                actions.append(TradeAction(player_no, -2, np.zeros(6, dtype=int), in_res))
        if len(actions) == 0:
            actions = [Action(player_no, ActionType.DECLINE)]
        return actions

    @classmethod
    def get_possible_setup_actions(cls,game_state:GameState):
        current_player = game_state.current_player
        road_next = game_state.players[current_player].settlement_count > len(game_state.players[current_player].roads)
        assert current_player >= 0; "No current player"
        if road_next:
            return cls.get_setup_road_actions(game_state,current_player)
        else:
            # no excess settlement
            return cls.get_setup_city_actions(game_state,current_player)

    def get_possible_base_actions(self, game_state:GameState) -> list[Action]:
        possible_trade_actions = self.get_possible_trade_actions(game_state)
        possible_build_actions = self.get_possible_build_actions(game_state)
        posible_card_actions = self.get_possible_card_actions(game_state, self.card_deck)
        possible_actions = [Action(game_state.current_player)]
        possible_actions += possible_trade_actions + possible_build_actions + posible_card_actions
        return possible_actions

    def get_possible_actions_main(self, game_state:GameState) -> list[Action]:
        player_no = game_state.current_player
        if game_state.phase == GamePhase.SETUP:
            return self.get_possible_setup_actions(game_state)
        if game_state.current_turn_moves == 0:
            return [DiceAction(player_no)]
        if len(game_state.discarding) > 0:
            p_id = game_state.discarding[0]
            return [
                DiscardAction(p_id,
                              game_state.players[p_id].resources[-1] // 2)]
        if game_state.robber_state == RobberState.PLACE_ROBBER:
            return self.get_possible_robber_placement_actions(game_state, player_no)
        if game_state.robber_state == RobberState.STEAL_RESOURCE:
            return self.get_possible_robber_steal_actions(game_state, player_no)
        if game_state.monopoly:
            return self.get_monopoly_actions(game_state, player_no)
        if game_state.year_of_plenty > 0:
            return self.get_year_of_plenty_actions(game_state, player_no)
        if game_state.road_building > 0:
            return self.get_possible_new_roads(game_state, player_no)
        return self.get_possible_base_actions(game_state)

    @classmethod
    def apply_setup_action(cls, game_state:GameState, action:Action):
        if isinstance(action,BuildCornerAction):
            BuildLogic.build_corner(game_state, action)
        elif isinstance(action,BuildEdgeAction):
            BuildLogic.build_edge(game_state, action)
            if game_state.current_player < len(game_state.players) - 1 and len(game_state.players[game_state.current_player].roads) == 1:
                #  Not all players have build a road
                game_state.current_player += 1
            elif len(game_state.players[game_state.current_player].roads) == 2 and game_state.current_player == 0:
                # All players build 2 roads
                game_state.current_turn_moves = 0
                game_state.phase = GamePhase.PLAY
                TurnLogic.initial_resources(game_state)
            elif len(game_state.players[game_state.current_player].roads) == 2:
                # Not all players have build their second road
                game_state.current_player -= 1
        else:
            raise Exception("Unknown setup action")
    

    @classmethod
    def apply_action(cls, game_state:GameState, action:Action) -> None:
        if game_state.phase == GamePhase.SETUP:
            cls.apply_setup_action(game_state, action)
            return 
        if action.action_type == ActionType.PASS:
            game_state.current_turn_moves = 0
            game_state.current_player = (game_state.current_player + 1) % len(game_state.players)
            return 
        game_state.current_turn_moves += 1
        if action.action_type == ActionType.DECLINE:
            game_state.robber_state = RobberState.NO_STATE
            game_state.trade_ongoing = False
            game_state.monopoly = False
            game_state.year_of_plenty = 0
            game_state.road_building = 0
        elif isinstance(action, BuildCornerAction):
            BuildLogic.build_corner(game_state, action)
        elif isinstance(action, BuildEdgeAction):
            BuildLogic.build_edge(game_state,  action)
        elif isinstance(action, DiceAction):
            TurnLogic.apply_dice(game_state, action)
        elif isinstance(action, PhaseAction):
            TurnLogic.phase_change(game_state, action)
        elif isinstance(action, TradeAction):
            TradeLogic.apply_trade(game_state, action)
        elif isinstance(action, RobberAction):
            TurnLogic.handle_robber_action(game_state, action)
        elif isinstance(action, CardAction):
            if action.draw:
                CardLogic.add_card(game_state, action)
            else:
                CardLogic.play_card(game_state, action)
        elif isinstance(action, RoadChangeAction):
            BuildLogic.apply_longest_road(game_state, action)
        elif isinstance(action, DiscardAction):
            TurnLogic.apply_discard_action(game_state, action)
        else:
            raise ValueError("Unkown action type")
        # assert game_state.check_integrity()
    
    @classmethod
    def sim_apply_setup_action(cls, game_state:GameState, action: Action):
        if isinstance(action,BuildCornerAction):
            return SimBuildLogic.build_corner(game_state, action)
        elif isinstance(action,BuildEdgeAction):
            game_state = SimBuildLogic.build_edge(game_state, action)
            if game_state.current_player < len(game_state.players) - 1 and len(game_state.players[game_state.current_player].roads) == 1:
                #  Not all players have build a road
                game_state.current_player += 1
            elif len(game_state.players[game_state.current_player].roads) == 2 and game_state.current_player == 0:
                # All players build 2 roads
                game_state.current_turn_moves = 0
                game_state.phase = GamePhase.PLAY
                SimTurnLogic.initial_resources(game_state)
            elif len(game_state.players[game_state.current_player].roads) == 2:
                # Not all players have build their second road
                game_state.current_player -= 1
            return game_state
        else:
            raise Exception("Unknown setup action")
    
    @classmethod
    def sim_apply_action(cls, game_state:GameState, action:Action) -> GameState:
        game_state = copy.copy(game_state)
        if game_state.phase == GamePhase.SETUP:
            return cls.sim_apply_setup_action(game_state, action)
        if action.action_type == ActionType.PASS:
            game_state.current_turn_moves = 0
            game_state.current_player = (game_state.current_player + 1) % len(game_state.players)
            return game_state
        game_state.current_turn_moves += 1
        if action.action_type == ActionType.DECLINE:
            game_state.robber_state = RobberState.NO_STATE
            game_state.monopoly = False
            game_state.year_of_plenty = 0
            game_state.road_building = 0
            return game_state
        elif isinstance(action, BuildCornerAction):
            return SimBuildLogic.build_corner(game_state, action)
        elif isinstance(action, BuildEdgeAction):
            return SimBuildLogic.build_edge(game_state,  action)
        elif isinstance(action, DiceAction):
            return SimTurnLogic.apply_dice(game_state, action)
        elif isinstance(action, PhaseAction):
            return SimTurnLogic.phase_change(game_state, action)
        elif isinstance(action, TradeAction):
            return SimTradeLogic.apply_trade(game_state, action)
        elif isinstance(action, RobberAction):
            return SimTurnLogic.handle_robber_action(game_state, action)
        elif isinstance(action, CardAction):
            if action.draw:
                return SimCardLogic.add_card(game_state, action)
            else:
                return SimCardLogic.play_card(game_state, action)
        elif isinstance(action, RoadChangeAction):
            return SimBuildLogic.apply_longest_road(game_state, action)
        elif isinstance(action, DiscardAction):
            return SimTurnLogic.apply_discard_action(game_state, action)
        raise Exception(f"Unknown action type {action}")

    def process_action(self, game_state:GameState, action:Action)-> tuple[Action, None|Action|list[Action]]:
        if action.action_type == ActionType.PASS:
            if self.check_victory(game_state):
                return PhaseAction(action.player_no,GamePhase.ENDED,[p.victory_points + p.development_cards[DevelopmentCard.VICTORY_POINT] for p in game_state.players]), None
            else:
                return action, None
        elif isinstance(action,  DiceAction):
            return TurnLogic.throw_dice(action), None
        elif isinstance(action, RobberAction):
            if action.robber_type == RobberActionType.STEAL:
                assert action.target_player != -1 
                target = game_state.players[action.target_player]
                if target.resources[-1] > 0:
                    resource = np.random.choice(np.where(target.resources[:-1] > 0)[0])
                    stolen_res = np.zeros(6, dtype=int)
                    stolen_res[[resource,-1]] = 1
                    return action, TradeAction(action.player_no, action.target_player, self.zeroes, stolen_res) # TODO double check if this works as intended
                return action, None
            else:
                return action, None
        if action.action_type == ActionType.DECLINE:
            return action, None
        if isinstance(action, BuildCornerAction) or isinstance(action, BuildEdgeAction):
            road_change = HelperLogic.update_longest_road(game_state, action.player_no)
            return action, road_change
        if isinstance(action,TradeAction):
            # Harbor Trade
            if action.target_player == -1:
                return action, None
            # Monopol
            elif action.target_player == -2:
                trades = []
                resource = np.argmax(action.in_resources)
                for i, player in enumerate(game_state.players):
                    if i != action.player_no:
                        out_res = np.zeros(6, dtype=int)
                        out_res[[resource,-1]] = player.resources[resource]
                        trades.append(TradeAction(i,-1,out_res,self.zeroes))
                player_trade = TradeAction(action.player_no,-1,self.zeroes, action.in_resources)
                trades.append(player_trade)
                return Action(action.player_no, ActionType.DECLINE), trades
            # Player to Player  Trade
            elif action.target_player >= 0 and not game_state.trade_ongoing:
                complement_action = TradeAction(
                    action.target_player, 
                    action.player_no, 
                    action.in_resources, 
                    action.out_resources
                )
                return action, [Action(action.target_player, ActionType.DECLINE), complement_action]
            else:
                return action, None
        if isinstance(action,CardAction):
            if action.draw:
                action = CardLogic.draw_card(self.card_deck, action)
                return action, None
            else:
                return action, None
        if isinstance(action, DiscardAction):
            return action, None

        # to be replaced by a general return action:
        
        # Should be changed to return after all actions are handled
        raise NotImplementedError