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

class TurnLogic:
    def __init__(self) -> None:
        pass

    @staticmethod
    def throw_dice(action:DiceAction) -> DiceAction:
        dice = np.random.randint(1, 7,2).sum()
        action.dice_value = dice
        return action
    
    @classmethod
    def initial_resources(cls, game_state:GameState):
        for player in game_state.players:
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
            HelperLogic.update_resources(game_state, player, resources)

    @classmethod
    def handle_robber_action(cls, game_state:GameState, action:RobberAction) -> None:
        assert isinstance(action, RobberAction)
        if action.robber_type == RobberActionType.PLACE:
            assert action.tile is not None
            game_state.robber_tile = action.tile.pos
            # TODO check if there is somebody to steal from
            game_state.robber_state = RobberState.STEAL_RESOURCE
        elif action.robber_type == RobberActionType.STEAL:
            game_state.robber_state = RobberState.NO_STATE


    @classmethod
    def apply_dice(cls, game_state:GameState, action:DiceAction):
        player = game_state.players[action.player_no]
        game_state.last_roll = action.dice_value
        player.development_cards += player.blocked_dev_cards
        player.blocked_dev_cards.fill(0)
        player.dev_card_played = False
        if action.player_no == 0:
            game_state.turn += 1
        if action.dice_value == 7:
            game_state.robber_state = RobberState.PLACE_ROBBER
            discarding_players =  np.argwhere([p.resources[-1] > RES_LIMIT for p in game_state.players])
            if len(discarding_players) > 0:
                game_state.discarding = discarding_players[0].tolist()
            return
        res_changes = np.zeros((len(game_state.players),6), dtype=int)
        for tile_id in game_state.board.dicemap[action.dice_value]:
            if tile_id == game_state.robber_tile:
                continue
            corners = game_state.board.cornermap[tile_id]
            for corner_id in corners:
                corner = game_state.board.corners[corner_id]
                if corner.building.player_no >= 0:
                    tile = game_state.board.get_tile_by_id(tile_id)
                    assert tile is not None
                    if corner.building.building_id in [BuildingType.SETTLEMENT, BuildingType.HARBOR_SETTLEMENT]:
                        res_changes[corner.building.player_no][tile.terrain.value] += 1
                    elif corner.building.building_id in [BuildingType.CITY, BuildingType.HARBOR_CITY]:
                        res_changes[corner.building.player_no][tile.terrain.value] += 2
        for i,player in enumerate(game_state.players):
            HelperLogic.update_resources(game_state, player, res_changes[i])
        return
    
    @staticmethod
    def phase_change(game_state:GameState, action:PhaseAction):
        game_state.phase = action.game_phase
        if game_state.phase == GamePhase.PLAY:
            TurnLogic.initial_resources(game_state)
            return
        if game_state.phase == GamePhase.ENDED:
            assert action.vp_update is not None
            for player,vp in zip(game_state.players, action.vp_update):
                player.victory_points = vp
            return
        return
    
    @staticmethod
    def apply_discard_action(game_state:GameState, action:DiscardAction):
        player = game_state.players[action.player_no]
        player.resources -= action.out_resources
        game_state.resources += action.out_resources
        game_state.discarding.remove(action.player_no)
        return