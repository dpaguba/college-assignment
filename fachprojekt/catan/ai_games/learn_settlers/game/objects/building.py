import numpy as np
from enum import IntEnum


class BuildingType(IntEnum):
    EMPTY = 0
    SETTLEMENT = 1
    CITY = 2
    ROAD = 3
    HARBOR = 4
    HARBOR_SETTLEMENT = 5
    HARBOR_CITY = 6

class Building:
    def __init__(self, player_no = -1, building_type = BuildingType.EMPTY, resource = None) -> None:
        self.player_no:int = player_no
        self.building_id:BuildingType = building_type
        if resource is None:
            self.resources: np.ndarray|None = None
        else:
            self.resources: np.ndarray|None = np.array(resource)

    def build(self, player_no:int, building_type:BuildingType):
        self.player_no = player_no
        if self.building_id == BuildingType.HARBOR and building_type == BuildingType.SETTLEMENT:
            self.building_id = BuildingType.HARBOR_SETTLEMENT
        elif self.building_id == BuildingType.HARBOR_SETTLEMENT and building_type == BuildingType.CITY:
            self.building_id = BuildingType.HARBOR_CITY
        else:
            self.building_id = building_type

    def __str__(self) -> str:
        return f"{self.building_id.name} {f'P:{self.player_no}' if self.player_no >= 0 else ''} {self.resources if self.resources is not None else ''}"