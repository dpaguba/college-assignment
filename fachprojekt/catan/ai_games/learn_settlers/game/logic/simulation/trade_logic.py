import copy
import numpy as np

from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.trade_action import TradeAction
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats


class SimTradeLogic:
    def __init__(self) -> None:
        pass


    @classmethod
    def apply_trade(cls, game_state:GameState, action:TradeAction):
        target_id = action.target_player
        # Trade is proposed to the other player but still needs to be approved by the other player
        if target_id >= 0 and action.player_no == game_state.current_player:
                game_state.trade_ongoing = True
                return game_state
        game_state.players = copy.copy(game_state.players)
        player = copy.copy(game_state.players[action.player_no])
        game_state.players[action.player_no] = player
        if target_id >= 0:
            game_state.trade_ongoing = False
            target = copy.copy(game_state.players[target_id])
            game_state.players[target_id] = target
            player.resources = player.resources - action.out_resources + action.in_resources
            target.resources = target.resources + action.out_resources - action.in_resources
        if target_id == -1:
            # Harbor Trade
            if game_state.year_of_plenty > 0:
                game_state.year_of_plenty -= 1
            player.resources = player.resources - action.out_resources + action.in_resources
            game_state.resources = game_state.resources + action.out_resources - action.in_resources
            # game_state.check_integrity()
        elif target_id == -2:
            # Monopol
            raise ValueError("Trade action not evaluated")
        return game_state

