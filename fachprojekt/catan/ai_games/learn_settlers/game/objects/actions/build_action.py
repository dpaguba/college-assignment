

from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType
from ai_games.learn_settlers.game.objects.board import Corner, Edge
from ai_games.learn_settlers.game.objects.building import BuildingType


class BuildCornerAction(Action):
    def __init__(self, player_no:int, corner, building_type, free = False):
        super().__init__(player_no, ActionType.BUILD)
        self.corner:Corner = corner
        self.building_type:BuildingType = building_type
        self.free = free
 
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BuildCornerAction):
            return False
        return super().__eq__(value) and self.corner == value.corner and self.building_type == value.building_type and self.free == value.free

    def __str__ (self):
        return f"{super().__str__()} {self.corner} {self.building_type.name} {'free' if self.free else ''}"

class BuildEdgeAction(Action):
    def __init__(self, player_no:int, edge, building_type, free=False):
        super().__init__(player_no, ActionType.BUILD)
        self.edge:Edge = edge
        self.building_type:BuildingType = building_type
        self.free=free

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BuildEdgeAction):
            return False
        return super().__eq__(value) and self.edge == value.edge and self.building_type == value.building_type and self.free == value.free

    def __str__ (self):
        return f"{super().__str__()} {self.edge} {self.building_type.name} {'free' if self.free else ''}"
    
class RoadChangeAction(Action):
    def __init__(self, player_no:int, no_old:int, no_new:int):
        super().__init__(player_no, ActionType.ROADCHANGE)
        self.no_old = no_old
        self.no_new = no_new

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, RoadChangeAction):
            return False
        return super().__eq__(value) and self.no_old == value.no_old and self.no_new == value.no_new

    def __str__(self) -> str:
        return f"New longest road by player {self.no_new}"