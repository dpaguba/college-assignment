import random

from ai_games.learn_settlers.game.objects.actions.card_action import DevelopmentCard


class CardDeck:
    def __init__(self, stack: list[DevelopmentCard]|None = None) -> None:
        if stack is None:
            self.stack:list[DevelopmentCard] = []
            self.stack.extend([DevelopmentCard.KNIGHT]*14)
            self.stack.extend([DevelopmentCard.VICTORY_POINT]*5)
            self.stack.extend([DevelopmentCard.ROAD_BUILDING]*2)
            self.stack.extend([DevelopmentCard.YEAR_OF_PLENTY]*2)
            self.stack.extend([DevelopmentCard.MONOPOLY]*2)
            random.shuffle(self.stack)
        else:
            self.stack = stack

    def draw(self):
        return self.stack.pop()

    def to_dict(self):
        return dict()