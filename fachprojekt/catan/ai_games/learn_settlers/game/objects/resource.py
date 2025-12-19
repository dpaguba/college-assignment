from enum import IntEnum

class Resource(IntEnum):
    Wood = 0
    Brick = 1
    Sheep = 2
    Wheat = 3
    Ore = 4
    sum = 5

class ResourceChange:
    def __init__(self) -> None:
        player_id = 0
        resource_id = 0
        resource_count = 0

class ResoureceExchange:
    def __init__(self) -> None:
        self.player_id = 0
        self.offer:dict[Resource,int] = {}
        self.request:dict[Resource,int] = {}

class ResourceTrade:
    def __init__(self) -> None:
        self.offer_player_id = 0
        self.offer:dict[Resource,int] = {}
        self.request_player_id = 0
        self.request:dict[Resource,int] = {}
        self.accepted = False
