from copy import copy
from PySide6.QtCore import QBasicTimer, Property, Qt, QPointF, QRectF, QSizeF
from PySide6.QtGui import QColor, QFontMetrics, QPaintEngine, QPainter, QPalette, QPolygonF, QBrush, QFont, QTextItem, QPen
from PySide6.QtWidgets import QWidget
import numpy as np, math

from ai_games.learn_settlers.game.objects.board import Board, Corner, Edge
from ai_games.learn_settlers.game.objects.building import BuildingType
from ai_games.learn_settlers.game.objects.game_state import GameState
from ai_games.learn_settlers.game.objects.player_stats import PlayerStats
from ai_games.learn_settlers.game.objects.terrain import Terrain


HEX_ANGLES_RAD = [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]
COS_ANGLES = [np.cos(angle) for angle in HEX_ANGLES_RAD]
SIN_ANGLES = [np.sin(angle) for angle in HEX_ANGLES_RAD]


class Hexagon(QPolygonF):
    def __init__(self, side_length,  center,  parent=None):

        hex_corners_2d = [QPointF(center.x() + side_length * np.sin(angle), center.y() + side_length * np.cos(angle)) for angle in HEX_ANGLES_RAD]
        return super().__init__(hex_corners_2d)
    



class BoardWidget(QWidget):
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
        super().__init__(parent)
        self.game_state = GameState(-1,3, Board.generate_board(1,"random"))
        self.clicked:None|tuple[float,float] = None

    
    def set_board(self, game_state: GameState):
        self.game_state = game_state
        self.update()


    def hex_to_pixel(self, r, q) -> QPointF:
        size = self.width() / self.game_state.board.size / 2
        x = size * (np.sqrt(3) * q  +  np.sqrt(3)/2 * r)
        y = size * (3./2 * r) + size
        return QPointF(x, y)
    
    def pixel_to_hex(self,x,y):
        size = self.width() / self.game_state.board.size / 2
        q = (x * np.sqrt(3)/3 - (y-size) / 3) / size
        r = (y-size) * 2/3 / size
        return q,r
    
    def pixel_to_edge(self,x,y):
        x,y = self.pixel_to_hex(x,y)
        # TODO
        return x,y
    
    def pixel_to_corner(self,x,y):
        x,y = self.pixel_to_hex(x,y)
        # TODO
        return x,y
    

    def paint_corner(self, painter:QPainter,corner:Corner):
        painter.setPen(QPen(QColor(255, 255, 255),2))
        # try:
        player_no = corner.building.player_no
        fill = QBrush(self.PLAYER_COLORS[player_no])
        painter.setBrush(fill)
        # except AttributeError:
        #     fill = QBrush(QColor(255, 255, 255))
        #     painter.setBrush(fill)
        size = self.width() / self.game_state.board.size / 6
        center1 = self.hex_to_pixel(corner.tiles[0][0], corner.tiles[0][1])
        center2 = self.hex_to_pixel(corner.tiles[1][0], corner.tiles[1][1])
        center3 = self.hex_to_pixel(corner.tiles[2][0], corner.tiles[2][1])
        center = QPointF((center1.x()+center2.x()+center3.x())/3, (center1.y()+center2.y()+center3.y())/3)
        rect = QRectF(center, QSizeF(size,size))
        rect.translate(-size/2,-size/2)
        painter.drawRect(rect)
        if corner.building is not None:
            if corner.building.building_id == BuildingType.SETTLEMENT:
                painter.drawText(rect, Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter, f"S")
            elif corner.building.building_id == BuildingType.CITY:
                painter.drawText(rect, Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter, f"C")
            elif corner.building.building_id == BuildingType.HARBOR_SETTLEMENT:
                painter.drawText(rect, Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter, f"HS")
            elif corner.building.building_id == BuildingType.HARBOR_CITY:
                painter.drawText(rect, Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter, f"HC")

    def paint_edge(self, painter:QPainter, edge:Edge, side_length:float):
        if edge.building.building_id != BuildingType.HARBOR:
            player_no = edge.building.player_no
            painter.setPen(QPen(self.PLAYER_COLORS[player_no],4))
            center1 = self.hex_to_pixel(edge.tiles[0][0], edge.tiles[0][1])
            center2 = self.hex_to_pixel(edge.tiles[1][0], edge.tiles[1][1])
            # paint normal vector
            r = math.atan2(center2.y()-center1.y(),center2.x()-center1.x())
            r_h = r + np.pi/6
            r_l = r - np.pi/6
            p1 = QPointF(center1.x()+side_length*math.cos(r_h),center1.y()+side_length*math.sin(r_h))
            p2 = QPointF(center1.x()+side_length*math.cos(r_l),center1.y()+side_length*math.sin(r_l))
            #painter.drawLine(center1,center2)
            painter.drawLine(p1,p2)
        else:
            size = self.width() / self.game_state.board.size / 12
            tile = [x for x in edge.tiles if (tile:=self.game_state.board.tiles[x[0]][x[1]]) is not None and tile.terrain == Terrain.Water][0]
            center1 = self.hex_to_pixel(edge.tiles[0][0], edge.tiles[0][1])
            center2 = self.hex_to_pixel(edge.tiles[1][0], edge.tiles[1][1])
            # paint normal vector
            r = math.atan2(center2.y()-center1.y(),center2.x()-center1.x())
            r_h = r + np.pi/6
            r_l = r - np.pi/6
            p1 = QPointF(center1.x()+side_length*math.cos(r_h),center1.y()+side_length*math.sin(r_h))
            p2 = QPointF(center1.x()+side_length*math.cos(r_l),center1.y()+side_length*math.sin(r_l))
            p3 = self.hex_to_pixel(tile[0],tile[1])
            #painter.drawLine(center1,center2)
            assert edge.building.resources is not None
            min_res = edge.building.resources.min()
            harbor_type = np.where(edge.building.resources == min_res)[0]
            if len(harbor_type) == 1:
                harbor_type = harbor_type[0]
                fill = QBrush(self.TILE_COLORS[harbor_type])
                painter.setBrush(fill)
                painter.setPen(QPen(self.TILE_COLORS[harbor_type],4))
                painter.drawEllipse(p3, size,size)
                painter.drawLine(p1,p3)
                painter.drawLine(p2,p3)
            else:
                fill = QBrush(self.TILE_COLORS [-1])
                painter.setBrush(fill)
                painter.setPen(QPen(self.TILE_COLORS[-1],4))
                painter.drawLine(p1,p3)
                painter.drawLine(p2,p3)
                painter.drawEllipse(p3, size,size)


    def paintEvent(self, event):
        width = self.width()
        height = self.height()

        # hexagon_width = width / self.board.size
        # # length of the side of the hexagon
        # hexagon_side_length = hexagon_width / np.sqrt(3)

        hexagon_height = width / self.game_state.board.size
        hexagon_side_length = hexagon_height / 2
        hexagon_width = np.sqrt(3) * hexagon_side_length

        font = QFont()
        font.setPixelSize(20)
        with QPainter(self) as painter:
            painter.setFont(font)
            # Paint grid
            for r,row in enumerate(self.game_state.board.tiles):
                for q,tile in enumerate(row):
                    if tile is None:
                        continue
                    painter.setPen(QColor(255, 255, 255))
                    hex_center = self.hex_to_pixel(r, q)
                    hex = Hexagon(hexagon_side_length, hex_center)
                    color = self.TILE_COLORS[tile.terrain.value]
                    fill = QBrush(color)
                    painter.setBrush(fill)
                    painter.drawPolygon(hex)
                    painter.setPen(QColor(0, 0, 0))
                    w = 100
                    h = 50
                    #rec = QRectF(x-(w/2), y-(h/2),w,h)
                    rec = QRectF(hex_center, QSizeF(w,h))
                    rec.translate(-w/2,-h/2)
                    #x_pos,y_pos = self.game_state.board.get_arr_to_hex(q,r)
                    painter.drawText(rec, Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignHCenter, f"({q},{r})")
                    # painter.setPen(QColor(0, 0, 0))
                    painter.drawText(rec, Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter, f"{tile.dice}")
            
            # Print edges
            for edge in self.game_state.board.edges:
                self.paint_edge(painter,edge, hexagon_side_length)
            
            # Lazy low effort variant
            for harbor in self.game_state.board.harbors:
                self.paint_edge(painter,harbor, hexagon_side_length)

            # paint corners
            font.setPixelSize(12)
            for corner in self.game_state.board.corners:
                self.paint_corner(painter,corner)

            # Print Robber
            painter.setBrush(QBrush(QColor(0, 0, 0)))

            center = self.hex_to_pixel(self.game_state.robber_tile[0], self.game_state.robber_tile[1])
            painter.drawEllipse(center, 12, 12)

            # Print clicks
            if self.clicked is not None:
                x,y = self.clicked
                painter.setBrush(QBrush(QColor(255, 0, 0)))
                center = QPointF(x, y)
                painter.drawEllipse(center, 10, 10)
                self.clicked = None