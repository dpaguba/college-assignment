from enum import IntEnum

class MessageType(IntEnum):
    ACTIONLIST = 0
    SETUP = 1
    DICE = 3
    TRADE = 4
    ACTION = 5
    GAMESTATE = 6
