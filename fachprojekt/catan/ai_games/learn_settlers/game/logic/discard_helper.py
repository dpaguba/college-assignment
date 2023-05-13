import numpy as np
from ai_games.learn_settlers.game.logic.simulation.trade_logic import SimTradeLogic
from ai_games.learn_settlers.game.objects.actions import DiscardAction
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.trade_action import TradeAction
from ai_games.learn_settlers.game.objects.game_state import GameState

# This class proposes one Resource to discard at a time and accumulates them into one action
class DiscardHelper():
    def __init__(self, game_state:GameState, action:DiscardAction):
        self.player_no = action.player_no
        self.to_discard = action.discard_count
        self.available_resources = game_state.players[self.player_no].resources.copy()
        self.action = action
        
    def propose_discard(self) -> list[DiscardAction]:
        possible_discards = np.where(self.available_resources[:-1] > 0)[0]
        discard_actions:list[DiscardAction] = []
        for i in possible_discards:
            out_res = np.zeros(6, int)
            out_res[[i,-1]] = 1
            discard_actions.append(DiscardAction(self.player_no, 1, out_res))
        return discard_actions
    
    # returns true while more cards need to be discarded
    def apply_discard(self, action:DiscardAction) -> bool:
        self.to_discard -= action.out_resources[-1]
        self.action.out_resources += action.out_resources
        self.available_resources -= action.out_resources
        return self.to_discard > 0
    
    def get_action(self) -> DiscardAction:
        return self.action