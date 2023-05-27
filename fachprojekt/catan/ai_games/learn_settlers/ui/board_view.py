from copy import copy
from PySide6.QtCore import QBasicTimer, Property, Qt, QPointF, QRectF, QSizeF, QObject, QLineF
from PySide6.QtGui import QColor, QFontMetrics, QPaintEngine, QPainter, QPalette, QPolygonF, QBrush, QFont, QTextItem, QPen, QMouseEvent
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsSimpleTextItem, QGraphicsTextItem, QWidget, QGraphicsWidget, QGraphicsView, QGraphicsScene, QLabel
import numpy as np, math

from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.build_action import BuildCornerAction, BuildEdgeAction
from ai_games.learn_settlers.game.objects.actions.robber_action import RobberAction, RobberActionType
from ai_games.learn_settlers.game.objects.board import Board, Corner, Edge
from ai_games.learn_settlers.game.objects.board_objects import Tile
from ai_games.learn_settlers.game.objects.building import BuildingType
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats
from ai_games.learn_settlers.game.objects.terrain import Terrain


HEIGHT = 1000
WIDTH = 1000

HEX_ANGLES_RAD = [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]
COS_ANGLES = [np.cos(angle) for angle in HEX_ANGLES_RAD]
SIN_ANGLES = [np.sin(angle) for angle in HEX_ANGLES_RAD]

class Hexagon(QPolygonF):
    # size of hex based on side length
    def __init__(self, hex_size,  center):
        hex_corners_2d = [QPointF(center.x() + hex_size * np.sin(angle), center.y() + hex_size * np.cos(angle)) for angle in HEX_ANGLES_RAD]
        return super().__init__(hex_corners_2d)
    
class BoardScene(QGraphicsScene):
    def __init__(self, sceneRect:QRectF, parent: QObject | None = None):
        super().__init__(sceneRect, parent)

class GrapicText(QGraphicsTextItem):
    my_font = QFont("Sans Serif",20)
    def __init__(self, center:QPointF, text, parent):
        super().__init__(text,parent)
        self.setFont(self.my_font)
        self.setDefaultTextColor(QColor(0, 0, 0))
        self.setPos(center.x()-30,center.y()-20)
        self.setAcceptedMouseButtons(Qt.MouseButton.NoButton)


class GraphicTile(QGraphicsPolygonItem):
    text_font = QFont("Sans Serif",20)
    def __init__(self, tile:Tile,  hex_center:QPointF, size:float, brush):
        hex = Hexagon(size,hex_center)
        super().__init__(hex)
        self.id = tile.pos
        self.setPen(QColor(255, 255, 255))
        self.setBrush(brush)
        self.label = GrapicText(hex_center,f"({str(tile.pos.r)},{str(tile.pos.q)}) \n {tile.dice}",self)

class GraphicEdge(QGraphicsLineItem):
    def __init__(self, id, line:QLineF, pen:QPen):
        super().__init__(line)
        self.setPen(pen)
        self.id = id

class GraphicSimpleText(QGraphicsSimpleTextItem):
    def __init__(self, id,x,y,parent):
        match id:
            case BuildingType.SETTLEMENT:
                text = " S"
            case BuildingType.CITY:
                text = " C"
            case BuildingType.HARBOR_SETTLEMENT:
                text = "HS"
            case BuildingType.HARBOR_CITY:
                text = "HC"
            case _:
                text = ""
        super().__init__(text, parent)
        self.setBrush(QColor(255, 255, 255))
        self.setPos(x,y)
        self.setAcceptedMouseButtons(Qt.MouseButton.NoButton)

class GraphicCorner(QGraphicsRectItem):
    def __init__(self, corner: Corner, center:QPointF, size:float, color):
        rect = QRectF(center, QSizeF(size,size))
        rect.translate(-size/2,-size/2)
        super().__init__(rect)
        self.setPen(QColor(255, 255, 255))
        self.setBrush(color)
        self.id = corner.id
        self.label = GraphicSimpleText(corner.building.building_id,rect.x(),rect.y(), self)

class BoardView(QGraphicsView):
    TILE_COLORS = [
        QColor(148, 193, 164), # Wood
        QColor(195, 163, 152), # Clay
        QColor(144, 211, 85), # Sheap
        QColor(255, 236, 161), # Wheat
        QColor(130, 130, 130), # Ore
        QColor(220, 220, 200), # Desert
        QColor(153 , 153, 250), # Water
        QColor(255, 255, 255) # White NPC
    ]
    PLAYER_COLORS = [
        QColor(160, 0, 0), # Red
        QColor(40, 150, 0), # Green
        QColor(0, 0, 160), # Blue
        QColor(0, 0, 0), # Magenta
        QColor(0, 0, 0), # Not used
        QColor(0, 0, 0), # Not used
        QColor(255, 255, 255),  # White NPC
    ]
    def __init__(self, parent: QWidget | None = None) -> None:
        scene_rect = QRectF(0,0,WIDTH,HEIGHT)
        self.board_scene = BoardScene(scene_rect)
        super().__init__(self.board_scene,parent)
        self.game_state = GameState(-1,-1, Board.generate_board(1,"empty"))
        self.hex_size = HEIGHT / self.game_state.board.size / 2
        self.text_font = QFont()
        self.text_font.setPixelSize(20)
        self.clicked:None|tuple[float,float] = None
        self.tiles: list[list[None | GraphicTile]] = [[]]
        self.edges:list[GraphicEdge] = []
        self.corners:list[GraphicCorner] = []
        self.robber:QGraphicsEllipseItem = self.set_robber((0,0), self.board_scene)

    
    def set_board(self, game_state: GameState):
        self.board_scene.clear()
        self.game_state = game_state
        self.hex_size = HEIGHT / self.game_state.board.size / 2
        self.tiles = [[self.add_tile(tile,self.board_scene) for tile in row] for row in self.game_state.board.tiles]
        for harbor in self.game_state.board.harbors:
            self.add_harbor(harbor, self.board_scene)
        self.robber:QGraphicsEllipseItem = self.set_robber(self.game_state.robber_tile, self.board_scene)
        self.edges = [self.add_edge(edge, self.board_scene) for edge in self.game_state.board.edges]
        self.corners = [self.add_corner(corner, self.board_scene) for corner in self.game_state.board.corners]

    def update_board(self, action:Action):
        player_no = action.player_no
        if isinstance(action,BuildCornerAction):
            corner_ref = self.corners[action.corner.id]
            corner_ref.setBrush(QBrush(self.PLAYER_COLORS[player_no]))
            match action.corner.building.building_id:
                case BuildingType.SETTLEMENT:
                    text = " S"
                case BuildingType.CITY:
                    text = " C"
                case BuildingType.HARBOR_SETTLEMENT:
                    text = "HS"
                case BuildingType.HARBOR_CITY:
                    text = "HC"
                case _:
                    text = ""
            corner_ref.label.setText(text)
        elif isinstance(action,BuildEdgeAction):
            edge_ref = self.edges[action.edge.id]
            edge_ref.setPen(QPen(self.PLAYER_COLORS[player_no],4))
        else:
            print(action)
            raise NotImplementedError
    
    def update_robber(self, action:RobberAction):
        robber_ref = self.robber
        r,q = action.tile.pos
        point = self.hex_to_pixel(r,q)
        robber_ref.setPos(point.x(),point.y())


    # Hex center point
    def hex_to_pixel(self, r:int, q:int) -> QPointF:
        x = self.hex_size * (np.sqrt(3) * q  +  np.sqrt(3)/2 * r)
        y = self.hex_size * (3./2 * r) + self.hex_size
        return QPointF(x, y)

    def set_robber(self, robber:tuple[int,int], scene:BoardScene) -> QGraphicsEllipseItem:
        pen = QPen(QColor(255,255,255),2)
        color = QColor(0,0,0)
        rect = QRectF(QPointF(-self.hex_size/6,-self.hex_size/6), QSizeF(self.hex_size/3,self.hex_size/3))
        robber_ref =  scene.addEllipse(rect, pen, color)
        point = self.hex_to_pixel(robber[0],robber[1])
        robber_ref.setPos(point.x(),point.y())
        return robber_ref

    def add_tile(self, tile:Tile|None, scene:BoardScene):
        if tile is None:
            return None
        hex_center = self.hex_to_pixel(*tile.pos)
        color = self.TILE_COLORS[tile.terrain.value]
        gtile = GraphicTile(tile, hex_center,self.hex_size, color)
        scene.addItem(gtile)
        return gtile

    def add_edge(self,edge:Edge, scene:BoardScene):
        # Normal building
        assert edge.building.building_id != BuildingType.HARBOR
        player_no = edge.building.player_no
        pen = QPen(self.PLAYER_COLORS[player_no],8)
        center1 = self.hex_to_pixel(edge.tiles[0][0], edge.tiles[0][1])
        center2 = self.hex_to_pixel(edge.tiles[1][0], edge.tiles[1][1])
        # paint normal vector
        r = math.atan2(center2.y()-center1.y(),center2.x()-center1.x())
        r_h = r + np.pi/6
        r_l = r - np.pi/6
        p1 = QPointF(center1.x()+self.hex_size*math.cos(r_h),center1.y()+self.hex_size*math.sin(r_h))
        p2 = QPointF(center1.x()+self.hex_size*math.cos(r_l),center1.y()+self.hex_size*math.sin(r_l))
        #painter.drawLine(center1,center2)
        line = QLineF(p1,p2)
        line_item = GraphicEdge(edge.id,line,pen)
        scene.addItem(line_item)
        return line_item

    def add_harbor(self, harbor:Edge, scene:BoardScene):
        # always true for just 1 Tile
        tile = [x for x in harbor.tiles if (tile:=self.game_state.board.tiles[x[0]][x[1]]) is not None and tile.terrain == Terrain.Water][0]
        center1 = self.hex_to_pixel(harbor.tiles[0][0], harbor.tiles[0][1])
        center2 = self.hex_to_pixel(harbor.tiles[1][0], harbor.tiles[1][1])
        # paint normal vector
        r = math.atan2(center2.y()-center1.y(),center2.x()-center1.x())
        r_h = r + np.pi/6
        r_l = r - np.pi/6
        p1 = QPointF(center1.x()+self.hex_size*math.cos(r_h),center1.y()+self.hex_size*math.sin(r_h))
        p2 = QPointF(center1.x()+self.hex_size*math.cos(r_l),center1.y()+self.hex_size*math.sin(r_l))
        p3 = self.hex_to_pixel(tile[0],tile[1])
        assert harbor.building.resources is not None
        min_res = harbor.building.resources.min()
        harbor_type = np.where(harbor.building.resources == min_res)[0]
        if len(harbor_type) == 1:
            color = self.TILE_COLORS[harbor_type[0]]
        else:
            color = self.TILE_COLORS[-1]
        pen = QPen(color,4)
        l1 = QLineF(p1,p3)
        l2 = QLineF(p2,p3)
        l1_ref = scene.addLine(l1, pen)
        l1_ref.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        l2_ref = scene.addLine(l2, pen)
        l2_ref.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        rect = QRectF(p3, QSizeF(self.hex_size/3,self.hex_size/3))
        rect.translate(-self.hex_size/6,-self.hex_size/6)
        harbor_ref = scene.addEllipse(rect, pen, color)
        harbor_ref.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
    

    def add_corner(self, corner:Corner, scene:BoardScene):
        player_no = corner.building.player_no
        color = QColor(255, 255, 255)
        pen = QPen(color, 2)
        brush = QBrush(self.PLAYER_COLORS[player_no])
        corner_size = self.hex_size / 4
        center1 = self.hex_to_pixel(corner.tiles[0][0], corner.tiles[0][1])
        center2 = self.hex_to_pixel(corner.tiles[1][0], corner.tiles[1][1])
        center3 = self.hex_to_pixel(corner.tiles[2][0], corner.tiles[2][1])
        center = QPointF((center1.x()+center2.x()+center3.x())/3, (center1.y()+center2.y()+center3.y())/3)
        rect_item = GraphicCorner(corner, center, corner_size, brush)
        scene.addItem(rect_item)
        return rect_item
    
    def mousePressEvent(self, event:QMouseEvent):
        item = self.itemAt(event.pos())
        while (parent:=item.parentItem()) is not None:
            item = parent
        print(item)

