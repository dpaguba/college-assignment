from collections import namedtuple
from ai_games.learn_settlers.game.objects.building import Building
from ai_games.learn_settlers.game.objects.terrain import Terrain

Pos = namedtuple("Pos", ["r","q"])

class Tile:
    def __init__(self, r:int, q:int, terrain_type:Terrain, dice:int):
        self.pos = Pos(r,q)
        self.terrain = terrain_type
        self.dice = dice

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Tile):
            return False
        return self.pos.q == value.pos.q and self.pos.r == value.pos.r
    
    def __hash__(self) -> int:
        return hash(self.pos)
    
    def __str__(self) -> str:
        return f"({self.pos.r},{self.pos.q})"

class Corner:
    def __init__(self, id:int, hexagon_id:Pos, hexagon2_id:Pos, hexagon3_id:Pos, building:Building|None = None):
        self.id = id
        self.tiles = (hexagon_id, hexagon2_id, hexagon3_id)
        if building is None:
            building = Building()
        self.building:Building = building

    def diff(self, corner:"Corner"):
        sum = 0
        if not corner.tiles[0] in self:
            sum += 1
        if not corner.tiles[1] in self:
            sum += 1
        if not corner.tiles[2] in self:
            sum += 1
        return sum

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Corner):
            return False
        return self.id == value.id
    
    def __hash__(self) -> int:
        return self.id
    
    def __contains__(self, hexagon:tuple[int,int]):
        return self.tiles[0] == hexagon or self.tiles[1] == hexagon or self.tiles[2] == hexagon
    
    def __str__(self) -> str:
        return f"[({self.tiles[0].r},{self.tiles[0].q}),({self.tiles[1].r},{self.tiles[1].q}),({self.tiles[2].r},{self.tiles[2].q})]: {self.building}"
    
class Edge:
    def __init__(self, id:int, hexagon1_id:Pos, hexagon2_id:Pos, building:Building|None = None):
        self.id = id
        self.tiles = (hexagon1_id, hexagon2_id)
        if building is None:
            building = Building()
        self.building:Building = building

    # def neigbor(self, corner:Corner):
    #     return self.tiles[0] in corner and self.tiles[1] in corner

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Edge):
            return False
        return self.id == value.id
    
    def __hash__(self) -> int:
        return self.id

    def __contains__(self, hexagon:tuple[int,int]):
        return self.tiles[0] == hexagon or self.tiles[1] == hexagon
    
    def __str__(self) -> str:
        return f"[({self.tiles[0].r},{self.tiles[0].q}),({self.tiles[1].r},{self.tiles[1].q})]: {self.building}"