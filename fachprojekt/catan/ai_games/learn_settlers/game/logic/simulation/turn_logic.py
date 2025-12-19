import copy
import numpy as np

from ai_games.learn_settlers.game.logic.helper_logic import HelperLogic
from ai_games.learn_settlers.game.objects.actions.dice_action import DiceAction
from ai_games.learn_settlers.game.objects.actions.discard_action import DiscardAction
from ai_games.learn_settlers.game.objects.actions.phase_action import PhaseAction
from ai_games.learn_settlers.game.objects.actions.robber_action import RobberAction, RobberActionType
from ai_games.learn_settlers.game.objects.building import BuildingType
from ai_games.learn_settlers.game.objects.game_state import GamePhase, GameState, RobberState

RES_LIMIT = 7

class SimTurnLogic:
    def __init__(self) -> None:
        pass

    @staticmethod
    def throw_dice(action:DiceAction) -> DiceAction:
        dice = np.random.randint(1, 7,2).sum()
        action.dice_value = dice
        return action

    @classmethod
    def initial_resources(cls, game_state:GameState):
        game_state.players = copy.copy(game_state.players)
        for i in range(len(game_state.players)):
            player = copy.copy(game_state.players[i])
            game_state.players[i] = player
            last_settlement = player.buildings[-1]
            resources = np.zeros(6, dtype=int)
            for tile_id in game_state.board.corners[last_settlement].tiles:
                tile = game_state.board.tiles[tile_id[0]][tile_id[1]]
                assert tile is not None
                resource = tile.terrain
                # Exclude desert and Water
                if resource.value > 4:
                    continue
                resources[resource.value] += 1
            HelperLogic.sim_update_resources(game_state, player, resources)
        return game_state

    @classmethod
    def handle_robber_action(cls, game_state:GameState, action:RobberAction) -> GameState:
        assert isinstance(action, RobberAction)
        if action.robber_type == RobberActionType.PLACE:
            assert action.tile is not None
            game_state.robber_state = RobberState.STEAL_RESOURCE
            game_state.robber_tile = action.tile.pos
        elif action.robber_type == RobberActionType.STEAL:
            game_state.robber_state = RobberState.NO_STATE
        return game_state

    @classmethod
    def apply_dice(cls, game_state:GameState, action:DiceAction) -> GameState:
        players = copy.copy(game_state.players)
        game_state.players = players
        player = copy.copy(players[action.player_no])
        players[action.player_no] = player
        game_state.last_roll = action.dice_value
        player.development_cards = player.development_cards + player.blocked_dev_cards
        player.blocked_dev_cards = np.zeros(6, dtype=int)
        player.dev_card_played = False
        if action.player_no ==0:
            game_state.turn += 1
        if action.dice_value == 7:
            game_state.robber_state = RobberState.PLACE_ROBBER
            discarding_players =  np.argwhere([p.resources[-1] > RES_LIMIT for p in game_state.players])
            if len(discarding_players) > 0:
                game_state.discarding = discarding_players[0].tolist()
            return game_state
        res_changes = np.zeros((len(game_state.players),6), dtype=int)
        for tile_id in game_state.board.dicemap[action.dice_value]:
            if tile_id == game_state.robber_tile:
                continue
            corners = game_state.board.cornermap[tile_id]
            for corner_id in corners:
                corner = game_state.board.corners[corner_id]
                if corner.building.player_no >= 0:
                    tile = game_state.board.tiles[tile_id[0]][tile_id[1]]
                    assert tile is not None
                    if corner.building.building_id in [BuildingType.SETTLEMENT, BuildingType.HARBOR_SETTLEMENT]:
                        res_changes[corner.building.player_no][tile.terrain.value] += 1
                    elif corner.building.building_id in [BuildingType.CITY, BuildingType.HARBOR_CITY]:
                        res_changes[corner.building.player_no][tile.terrain.value] += 2
        for i in range(len(game_state.players)):
            if i != action.player_no:
                player = copy.copy(game_state.players[i])
                game_state.players[i] = player
            else:
                player = game_state.players[i]
            HelperLogic.sim_update_resources(game_state, player, res_changes[i])
        return game_state
    
    @staticmethod
    def phase_change(game_state:GameState, action:PhaseAction) -> GameState:
        game_state.phase = action.game_phase
        if game_state.phase == GamePhase.PLAY:
            return SimTurnLogic.initial_resources(game_state)
        if game_state.phase == GamePhase.ENDED:
            game_state.players = copy.copy(game_state.players)
            game_state.players = [copy.copy(p) for p in game_state.players]
            assert action.vp_update is not None
            for player,vp in zip(game_state.players, action.vp_update):
                player.victory_points = vp
            return game_state
        return game_state
    
    @staticmethod
    def apply_discard_action(game_state:GameState, action:DiscardAction):
        game_state.discarding = copy.copy(game_state.discarding)
        game_state.players = copy.copy(game_state.players)
        player = copy.copy(game_state.players[action.player_no])
        game_state.players[action.player_no] = player
        player.resources = player.resources - action.out_resources
        game_state.resources = game_state.resources + action.out_resources
        game_state.discarding.remove(action.player_no)
        return game_state
