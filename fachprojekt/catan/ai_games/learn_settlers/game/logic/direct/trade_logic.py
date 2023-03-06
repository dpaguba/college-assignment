import copy
import numpy as np

from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType
from ai_games.learn_settlers.game.objects.actions.trade_action import TradeAction
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats


class TradeLogic:
    def __init__(self) -> None:
        pass
    

    @classmethod
    def apply_trade(cls, game_state:GameState, action:TradeAction):
        player = game_state.players[action.player_no]
        target_id = action.target_player
        if target_id >= 0:
            if action.player_no == game_state.current_player:
                # Trade is proposed to the other player but still needs to be approved by the other player
                game_state.trade_ongoing = True
                return
            game_state.trade_ongoing = False
            target = game_state.players[target_id]
            player.resources = player.resources - action.out_resources + action.in_resources
            target.resources = target.resources - action.in_resources + action.out_resources
            return
        elif target_id == -1:
            # Harbor Trade
            if game_state.year_of_plenty > 0:
                game_state.year_of_plenty -= 1
            player.resources = player.resources - action.out_resources + action.in_resources
            game_state.resources = game_state.resources + action.out_resources - action.in_resources
            return
            # game_state.check_integrity()
        elif target_id == -2:
            # Monopol
            raise ValueError("Trade action not evaluated")
        raise ValueError("Trade action not evaluated")

