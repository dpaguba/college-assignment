import random, numpy as np
import typing

from ai_games.learn_settlers.com import Message
from ai_games.learn_settlers.game.objects.board_objects import Corner, Edge, Pos, Tile
from ai_games.learn_settlers.game.objects.building import Building, BuildingType
from ai_games.learn_settlers.game.objects.terrain import Terrain

NUMBERCHIPS = [11,3,6,5,4,9,10,8,4,11,12,9,10,8,3,6,2,5]
NUMBERORDER = [
            (1,3),(2,2),(3,1),(4,1),(5,1),(5,2),(5,3),(4,4),(3,5),(2,5),(1,5),(1,4),(2,3),(3,2),(4,2),(4,3),(3,4),(2,4),(3,3)  
        ]
TERRAINTYPES = [Terrain.Forest]*4 +[Terrain.Clay]*3 + [Terrain.Meadow]*4 + [Terrain.Wheat]*4 + [Terrain.Mountain]*3 + [Terrain.Desert]
HARBORS = [Building(building_type=BuildingType.HARBOR, resource=np.array([3 for _ in range(5)])) for _ in range(4)]
HARBORS += [Building(building_type=BuildingType.HARBOR, resource=np.array([4 if x != res else 2 for x in range(5)])) for res in range(5)]


class Board:
    def __init__(self, tiles, edges, corners, harbors):
        self.size = len(tiles)
        self.offset = self.size //2 
        self.tiles:list[list[Tile|None]] = tiles
        self.harbors:list[Edge] = harbors
        # Edges
        self.edgemap:dict[Pos,list[int]] = {}
        self.edges:list[Edge] = edges
        for edge in self.edges:
            for tile in edge.tiles:
                self.edgemap.setdefault(tile, []).append(edge.id)
        # Corners
        self.cornermap:dict[Pos,list[int]] = {}
        self.corners:list[Corner] = corners
        for corner in self.corners:
            for tile in corner.tiles:
                self.cornermap.setdefault(tile, []).append(corner.id)
        self.possible_settlements = set(corners)
        build_corners = set([c for c in self.corners if c.building.building_id != BuildingType.EMPTY and c.building.building_id != BuildingType.HARBOR])
        blocked = [c for bc in build_corners for c in self.corners if bc.diff(c) <= 1]
        if len(blocked) > 0:
            self.possible_settlements = self.possible_settlements.difference(blocked)
            

        for corner in self.corners:
            if corner.building.building_id != BuildingType.EMPTY and corner.building.building_id != BuildingType.HARBOR:
                buildings = [y  for x in corner.tiles for y  in self.cornermap[x]]
                buildings = [x for x in buildings if corner.diff(self.corners[x]) <= 1]
                self.possible_settlements = self.possible_settlements.difference(corners)

        # dice to tile map
        self.dicemap:list[list[Pos]] = [[] for _ in range(13)]
        for row in self.tiles:
            for tile in row:
                if tile is not None:
                    self.dicemap[tile.dice].append(tile.pos)
        
        # neighbors
        self.neighbor_edges:dict[int,set[int]] = {}
        self.neighbor_corners:dict[int,set[int]] = {}
        for corner in self.corners:
            nb_edge = self.neighbor_edges.setdefault(corner.id, set())
            edges = set([e for t in corner.tiles for e in self.edgemap[t] if self.edges[e].tiles[0] in corner.tiles and self.edges[e].tiles[1] in corner.tiles and self.edges[e].building.building_id != BuildingType.HARBOR])
            nb_edge.update([e for e in edges])
            for e in edges:
                nb_corner = self.neighbor_corners.setdefault(e, set())
                nb_corner.add(corner.id)
    
    def get_tile_by_id(self, tile_id: tuple[int,int]):
        tile = self.tiles[tile_id[0]][tile_id[1]]
        assert tile is None or tile_id == tile.pos
        return tile
    
    def get_corner(self,id:int) -> Corner:
        assert id >= 0
        return self.corners[id]
    
    def get_edge(self, id:int) -> Edge:
        assert id >= 0
        return self.edges[id]

    def get_hex_to_arr(self, x:int, y:int):
        return (x+self.offset, y+self.offset)

    def get_arr_to_hex(self, q:int, r:int):
        return (q-self.offset, r-self.offset)
    
    def get_neighbors_of_edge(self, edge_id:int) -> list[Corner]:
        return [self.corners[x] for x in self.neighbor_corners[edge_id]]

    def get_neighbors_of_corner(self, corner_id:int) -> list[Edge]:
        return [self.edges[x] for x in self.neighbor_edges[corner_id]]

    @classmethod
    @typing.no_type_check
    def from_msg(cls, msg:Message):
        tiles = [[(hexagon.type, hexagon.number) for hexagon in row] for row in msg.tiles]
        return cls(msg.size, tiles)

    @classmethod
    def generate_board(cls, size:int, type:str) -> "Board":
        size = size + 2
        if type == "random":
            tiles = cls.generate_random(size)
        elif type == "standard":
            tiles = cls.generate_standard(size)
        elif type == "empty":
            return Board([[Tile(0,0,Terrain.Desert,0)]],[],[],[])
        else:
            raise ValueError("Invalid board type")
        corners = cls.generate_corners(tiles)
        edges = cls.generate_edges(tiles)
        harbors = cls.populate_harbors(tiles, corners, edges)
        return Board(tiles, edges, corners, harbors)
    
    @staticmethod
    def arrage_tiles(size:int) -> list[list[Tile|None]]:
        offset = size //2
        tiles = [[
                Tile(r,
                     q,
                     Terrain.Desert,
                     0)
                     if q>=offset-r and q<=3*offset-r else None for q in range(size) ]for r in range(size)]
        # make edge tiles water
        for tile in tiles[0]:
            if tile is not None:
                tile.terrain = Terrain.Water
                tile.dice = 0
        for tile in tiles[-1]:
            if tile is not None:
                tile.terrain = Terrain.Water
                tile.dice = 0
        for row in tiles:
            # make first row of tiles water
            for tile in row:
                if tile is not None:
                    tile.terrain = Terrain.Water
                    tile.dice = 0
                    break
                else:
                    continue
            # make last row of tiles water
            for tile in reversed(row):
                if tile is not  None:
                    tile.terrain = Terrain.Water
                    tile.dice = 0
                    break
                else:
                    continue
        tile_types = TERRAINTYPES.copy()
        random.shuffle(tile_types)
        for row in tiles:
            for tile in row:
                if tile is None or tile.terrain == Terrain.Water:
                    continue
                tile.terrain = tile_types.pop()
        return tiles
    
    @classmethod
    def generate_standard(cls, size:int) -> list[list[Tile|None]]:
        tiles = cls.arrage_tiles(size)
        dice_values = NUMBERCHIPS.copy()
        for r,q in NUMBERORDER:
            tile = tiles[r][q]
            assert tile is not None
            assert tile.terrain != Terrain.Water
            if tile.terrain == Terrain.Desert:
                continue
            tile.dice = dice_values.pop()
        return tiles
    
    @staticmethod
    def check_numbers(tiles:list[list[Tile|None]]):
        for r, row in enumerate(tiles):
            for q, tile in enumerate(row):
                if tile is None or tile.terrain == Terrain.Water:
                    continue
                if tile.dice in [6,8]:
                    naighbors = [t for r_n, q_n in [(r+1,q),(r,q+1),(r-1,q),(r,q-1),(r-1,q+1),(r+1,q-1)] if (t:=tiles[r_n][q_n]) is not None]
                    if any([(t.dice in [6,8]) for t in naighbors]):
                        dice_val = tile.dice
                        r_a,q_a = random.randint(1,5),random.randint(1,5)
                        alt_tile = tiles[r_a][q_a]
                        while alt_tile is None or alt_tile.terrain in [Terrain.Water, Terrain.Desert]:
                            r_a,q_a = random.randint(1,5),random.randint(1,5)
                            alt_tile = tiles[r_a][q_a]
                        tile.dice = alt_tile.dice
                        alt_tile.dice = dice_val
                        return False
        return True
                    
    
    @classmethod
    def generate_random(cls, size:int) -> list[list[Tile|None]]:
        tiles = cls.arrage_tiles(size)
        dice_values = NUMBERCHIPS.copy()
        random.shuffle(dice_values)
        # Set dice values randomly
        for row in tiles:
            for tile in row:
                if tile is None or tile.terrain == Terrain.Water:
                    continue
                if tile.terrain == Terrain.Desert:
                    continue
                tile.dice = dice_values.pop()
        # prevent 6s and 8s next to each other
        valid = False
        while not valid:
            valid = cls.check_numbers(tiles)
        return tiles
    
    @staticmethod
    def generate_edges(tiles: list[list[Tile|None]]) -> list[Edge]:
        edges:list[Edge] = []
            # Add edges
            #  q,r 
            # +1, 0
            #  0,+1
            # -1,+1
        for r, row in enumerate(tiles):
            for q, tile in enumerate(row):
                if tile is None:
                    continue
                try:
                    alt_tile = tiles[r][q+1]
                except IndexError:
                    alt_tile = None
                if alt_tile is not None:
                    if tile.terrain != Terrain.Water or alt_tile.terrain != Terrain.Water:
                        edge = Edge(len(edges),tile.pos, alt_tile.pos)
                        edges.append(edge)
                try:
                    alt_tile = tiles[r+1][q]
                except IndexError:
                    alt_tile = None
                if alt_tile is not None:
                    if tile.terrain != Terrain.Water or alt_tile.terrain != Terrain.Water:
                        edge = Edge(len(edges), tile.pos, alt_tile.pos)
                        edges.append(edge)
                if q > 0:
                    try:
                        alt_tile = tiles[r+1][q-1]
                    except IndexError:
                        alt_tile = None
                    if alt_tile is not None:
                        if tile.terrain != Terrain.Water or alt_tile.terrain != Terrain.Water:
                            edge = Edge(len(edges), tile.pos, alt_tile.pos)
                            edges.append(edge)
        return edges

    @staticmethod
    def generate_corners(tiles:list[list[Tile|None]]) -> list[Corner]:
        # Add Corners
        #  q, r  | q, r
        # +1, 0  | 0,+1
        # -1,+1  | 0,+1
        corners:list[Corner] = []
        for r, row in enumerate(tiles):
            for q, tile in enumerate(row):
                if tile is None:
                    continue
                try:
                    alt_tile_1 = tiles[r][q+1]
                    alt_tile_2 = tiles[r+1][q]
                except IndexError:
                    alt_tile_1 = None
                    alt_tile_2 = None
                if alt_tile_1 is not None and alt_tile_2 is not None:
                    corner = Corner(len(corners), tile.pos, alt_tile_1.pos, alt_tile_2.pos)
                    corners.append(corner)
                if q > 0:
                    try:
                        alt_tile_1 = tiles[r+1][q]
                        alt_tile_2 = tiles[r+1][q-1]
                    except IndexError:
                        alt_tile_1 = None
                        alt_tile_2 = None
                    if alt_tile_1 is not None and alt_tile_2 is not None:
                        corner = Corner(len(corners), tile.pos, alt_tile_1.pos, alt_tile_2.pos)
                        corners.append(corner)
        return corners

    @staticmethod
    def populate_harbors(tiles:list[list[Tile|None]], corners:list[Corner],edges:list[Edge]):
        cornermap:dict[tuple[int,int],list[Corner]] = {}
        for corner in corners:
            for tile in corner.tiles:
                cornermap.setdefault(tile, []).append(corner)
        edgemap:dict[tuple[int,int],list[Edge]] = {}
        for edge in edges:
            for tile in edge.tiles:
                edgemap.setdefault(tile, []).append(edge)

        harbortiles:list[Tile] = []
        toggle = random.choice([True, False])
        for tile in tiles[0]:
                if tile is None:
                    continue
                if toggle:
                    toggle = False
                else:
                    toggle = True
                if tile.terrain == Terrain.Water:
                    if toggle:
                        harbortiles.append(tile)
                        #tile.type = Terrain.Desert

        for tile in tiles[-1]:
            if tile is None:
                continue
            if toggle:
                toggle = False
            else:
                toggle = True
            if tile.terrain == Terrain.Water:
                if toggle:
                    harbortiles.append(tile)
                    #tile.type = Terrain.Desert

        for row  in tiles[1:-1]:
            if toggle:
                for tile in row:
                    if tile is None:
                        continue
                    if tile.terrain == Terrain.Water:
                        harbortiles.append(tile)
                        #tile.type = Terrain.Desert
                        toggle = False
                        break
            else:
                for tile in reversed(row):
                    if tile is None:
                        continue
                    if tile.terrain == Terrain.Water:
                        harbortiles.append(tile)
                        #tile.type = Terrain.Desert
                        toggle = True
                        break
        
        harbors = HARBORS.copy()
        random.shuffle(harbors)
        harbor_edges:list[Edge] = []
        for harbor_tile in harbortiles:
            edge = random.choice(edgemap[harbor_tile.pos])
            corners = [y  for x in edge.tiles for y  in cornermap[x]]
            corners = [x for x in corners if edge.tiles[0] in x and edge.tiles[1] in x]
            building = harbors.pop()
            harbor = Edge(len(edges), edge.tiles[0], edge.tiles[1], building)
            harbor_edges.append(harbor)

            for corner in corners:
                corner.building.building_id = BuildingType.HARBOR
                corner.building.resources = building.resources
        return harbor_edges
