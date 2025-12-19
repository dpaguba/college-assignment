from enum import IntEnum
import typing
import numpy as np

from ai_games.learn_settlers.game.objects.actions.card_action import DevelopmentCard
from ai_games.learn_settlers.game.objects.board import Corner, Edge
from ai_games.learn_settlers.game.objects.resource import Resource


class PlayerStats:
    def __init__(self, player_name:str = "", victory_points:int = 0, resources:list[int]|None = None, development_cards:list[int]|None = None, buildings:list[int]|None = None, roads:list[int]|None = None, knights = 0, longest_road = False, largest_army = False, trade_costs = None, settlement_count = 0, city_count = 0, blocked_dev_cards:list[int]|None = None, dev_card_played:bool = False) -> None:
        self.player_name = player_name
        self.victory_points = victory_points
        if resources is None:
            resources = [0 for _ in Resource]
        self.resources = np.array(resources)
        if development_cards is None:
            development_cards = [0 for _ in DevelopmentCard]
        self.development_cards = np.array(development_cards,dtype=int)
        if blocked_dev_cards is None:
            blocked_dev_cards = [0 for _ in DevelopmentCard]
        self.blocked_dev_cards = np.array(blocked_dev_cards,dtype=int)
        self.dev_card_played = dev_card_played
        if buildings is None:
            buildings = []
        self.buildings: list[int] = buildings
        self.settlement_count = settlement_count
        self.city_count = city_count
        if roads is None:
            roads = []
        self.roads: list[int] = roads
        if trade_costs is None:
            trade_costs = [4,4,4,4,4]
        self.trade_costs = np.array(trade_costs)
        self.knights = knights
        self.longest_road = longest_road
        self.largest_army = largest_army
