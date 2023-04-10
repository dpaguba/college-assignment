

import numpy as np
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType
from ai_games.learn_settlers.game.objects.resource import Resource


class DiscardAction(Action):
    def __init__(self, player_no:int, discard_count:int, out_resources:np.ndarray|None = None):
        super().__init__(player_no, ActionType.DISCARD)
        self.discard_count = discard_count
        if out_resources is None:
            out_resources = np.zeros(6,int)
        self.out_resources:np.ndarray = out_resources

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DiscardAction):
            return False
        return super().__eq__(other) and self.discard_count == other.discard_count and all(self.out_resources == other.out_resources)

    def __str__(self):
        return f"{super().__str__()} COUNT:{self.discard_count} drop:{self.out_resources}"