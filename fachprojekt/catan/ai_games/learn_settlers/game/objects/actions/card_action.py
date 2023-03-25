

from enum import IntEnum
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType

class DevelopmentCard(IntEnum):
    KNIGHT = 0
    ROAD_BUILDING = 1
    YEAR_OF_PLENTY = 2
    MONOPOLY = 3
    VICTORY_POINT = 4
    SUM = 5

class CardAction(Action):
    def __init__(self, player_no:int, draw:bool, card_type:DevelopmentCard|None = None):
        super().__init__(player_no, ActionType.CARD)
        assert draw or (card_type is not None)
        self.draw = draw
        self.card_type = card_type
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, CardAction):
            return False
        return super().__eq__(value) and self.draw == value.draw and self.card_type == value.card_type

    def __str__(self):
        return f"{super().__str__()} {'Draw' if self.draw else 'Play'} {self.card_type.name if self.card_type else None}"
