
from enum import IntEnum
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType
from ai_games.learn_settlers.game.objects.board import Corner, Tile

class RobberActionType(IntEnum):
    PLACE = 0
    STEAL = 1



class RobberAction(Action):
    def __init__(self, player_no:int, robber_type: RobberActionType, tile:Tile, target_player:int = -1):
        super().__init__(player_no, ActionType.ROBBER)
        self.robber_type = robber_type
        self.tile = tile
        self.target_player = target_player

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RobberAction):
            return False
        return super().__eq__(other) and self.robber_type == other.robber_type and self.tile == other.tile and self.target_player == other.target_player

    def __str__(self):
        return f"{super().__str__()} {self.robber_type.name} {str(self.tile) if self.robber_type == RobberActionType.PLACE else f'T:{self.target_player}'}"