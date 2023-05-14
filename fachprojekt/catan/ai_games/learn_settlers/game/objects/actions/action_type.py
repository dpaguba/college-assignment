from enum import IntEnum

class ActionType(IntEnum):
    PASS = 0
    DICE = 1
    BUILD = 2
    TRADE = 3
    CARD = 4
    ROBBER = 5
    GAMEPHASE = 6
    ROADCHANGE = 7
    DECLINE = 8
    DISCARD = 9

