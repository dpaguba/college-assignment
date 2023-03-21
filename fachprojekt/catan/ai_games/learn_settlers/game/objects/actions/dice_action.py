

from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType


class DiceAction(Action):
    def __init__(self, player_no:int, dice_value:int = 0):
        super().__init__(player_no, ActionType.DICE)
        self.dice_value = dice_value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DiceAction):
            return False
        return super().__eq__(other) and self.dice_value == other.dice_value

    def __str__(self) -> str:
        return f"{super().__str__()} {self.dice_value}"