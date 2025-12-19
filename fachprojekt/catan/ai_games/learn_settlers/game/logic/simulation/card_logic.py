import copy
import numpy as np

from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.card_action import CardAction, DevelopmentCard
from ai_games.learn_settlers.game.objects.card_deck import CardDeck
from ai_games.learn_settlers.game.objects.game_state import GameState, RobberState


class SimCardLogic:
    def __init__(self) -> None:
        pass

    @classmethod
    def draw_card(cls, card_deck:CardDeck, action:CardAction) -> CardAction:
        # TODO remove side effects
        # TODO This funcion does not really serve a purpouse for simulation but should only be used when generating games with a new game state per turn.
        action.card_type = card_deck.draw()
        return action
    
    # Adjust for ng logic
    @classmethod
    def add_card(cls, original_game_state:GameState, action:CardAction) -> GameState:
        assert action.draw
        assert action.card_type is not None
        game_state = copy.copy(original_game_state)
        game_state.players = copy.copy(game_state.players)
        player = copy.copy(game_state.players[action.player_no])
        game_state.players[action.player_no] = player
        player.development_cards = copy.copy(player.development_cards)
        res_changes = np.array([0,0,1,1,1,3])
        player.resources = player.resources - res_changes
        game_state.resources = game_state.resources + res_changes
        new_card = action.card_type
        player.development_cards[-1]+=1
        if new_card == DevelopmentCard.VICTORY_POINT:
            player.development_cards[new_card.value] += 1
        else:
            player.blocked_dev_cards = copy.copy(player.blocked_dev_cards)
            player.blocked_dev_cards[new_card.value] += 1
        return game_state
    
    @classmethod
    def play_card(cls, game_state:GameState, action:CardAction):
        assert not action.draw
        assert action.card_type is not None
        game_state.players = copy.copy(game_state.players)
        player = copy.copy(game_state.players[action.player_no])
        game_state.players[action.player_no] = player
        player.dev_card_played = True
        player.development_cards = copy.copy(player.development_cards)
        if action.card_type == DevelopmentCard.KNIGHT:
            game_state.robber_state = RobberState.PLACE_ROBBER
            player.development_cards[[DevelopmentCard.KNIGHT.value,-1]] -= 1
            player.knights += 1
            if player.knights >= 3 and not player.largest_army and all([x.knights < player.knights for x in game_state.players if x is not player]):
                for i in range(len(game_state.players)):
                    p = game_state.players[i]
                    if p.largest_army:
                        game_state.players[i] = copy.copy(game_state.players[i])
                        game_state.players[i].largest_army = False
                        game_state.players[i].victory_points -= 2
                player.largest_army = True
                player.victory_points += 2
        elif action.card_type == DevelopmentCard.ROAD_BUILDING:
            game_state.road_building = 2
            player.development_cards[[DevelopmentCard.ROAD_BUILDING.value,-1]] -= 1
        elif action.card_type == DevelopmentCard.YEAR_OF_PLENTY:
            game_state.year_of_plenty = 2
            player.development_cards[[DevelopmentCard.YEAR_OF_PLENTY.value,-1]] -= 1
        elif action.card_type == DevelopmentCard.MONOPOLY:
            game_state.monopoly = True
            player.development_cards[[DevelopmentCard.MONOPOLY.value,-1]] -= 1
        return game_state