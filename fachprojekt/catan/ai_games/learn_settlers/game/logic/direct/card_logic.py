import copy
import numpy as np

from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.card_action import CardAction, DevelopmentCard
from ai_games.learn_settlers.game.objects.card_deck import CardDeck
from ai_games.learn_settlers.game.objects.game_state import GameState, RobberState


class CardLogic:
    def __init__(self) -> None:
        pass

    @classmethod
    def draw_card(cls, card_deck:CardDeck, action:CardAction) -> CardAction:
        action.card_type = card_deck.draw()
        return action

    @classmethod
    def add_card(cls, game_state:GameState,action:CardAction):
        assert action.draw
        assert action.card_type is not None
        player_no = action.player_no
        player = game_state.players[player_no]
        player.resources[[2,3,4]] -= 1
        player.resources[5] -= 3
        game_state.resources[[2,3,4]] += 1
        game_state.resources[5] += 3
        new_card = action.card_type
        player.development_cards[-1]+=1
        if new_card == DevelopmentCard.VICTORY_POINT:
            player.development_cards[new_card.value] += 1
        else:
            player.blocked_dev_cards[new_card.value] += 1


    @classmethod
    def play_card(cls, game_state:GameState, action:CardAction):
        assert not action.draw
        assert action.card_type is not None
        player_no = action.player_no
        player = game_state.players[player_no]
        player.dev_card_played = True
        if action.card_type == DevelopmentCard.KNIGHT:
            game_state.robber_state = RobberState.PLACE_ROBBER
            player.development_cards[[DevelopmentCard.KNIGHT.value,-1]] -= 1
            player.knights += 1
            if player.knights >= 3 and not player.largest_army and all([x.knights < player.knights for x in game_state.players if x is not player]):
                for p in game_state.players:
                    if p.largest_army:
                        p.largest_army = False
                        p.victory_points -= 2
                player.largest_army = True
                player.victory_points += 2
                return
        elif action.card_type == DevelopmentCard.ROAD_BUILDING:
            game_state.road_building = 2
            player.development_cards[[DevelopmentCard.ROAD_BUILDING.value,-1]] -= 1
        elif action.card_type == DevelopmentCard.YEAR_OF_PLENTY:
            game_state.year_of_plenty = 2
            player.development_cards[[DevelopmentCard.YEAR_OF_PLENTY.value,-1]] -= 1
        elif action.card_type == DevelopmentCard.MONOPOLY:
            game_state.monopoly = True
            player.development_cards[[DevelopmentCard.MONOPOLY.value,-1]] -= 1
        return None