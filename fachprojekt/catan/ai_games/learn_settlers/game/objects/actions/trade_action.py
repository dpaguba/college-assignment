

import numpy as np
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType
from ai_games.learn_settlers.game.objects.resource import Resource


class TradeAction(Action):
    def __init__(self, player_no:int, target_player:int, out_resources:np.ndarray, in_resources:np.ndarray):
        super().__init__(player_no, ActionType.TRADE)
        self.target_player = target_player
        self.out_resources = out_resources
        self.in_resources = in_resources

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TradeAction):
            return False
        return super().__eq__(other) and self.target_player == other.target_player and all(self.out_resources == other.out_resources) and all(self.in_resources == other.in_resources)

    def __str__(self):
        return f"{super().__str__()} T:{self.target_player} OUT:{self.out_resources} IN:{self.in_resources}"