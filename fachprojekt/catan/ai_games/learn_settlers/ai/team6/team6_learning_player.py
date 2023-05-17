from ai_games.learn_settlers.game.player.player import Player, PlayerType
from ai_games.learn_settlers.ai.team6.strategy_manager import StrategyManager
from ai_games.learn_settlers.com.message_type import MessageType
from ai_games.learn_settlers.game.objects.actions import Action
from ai_games.learn_settlers.game.objects.actions.phase_action import PhaseAction
from ai_games.learn_settlers.game.objects.game_state import GameState

import random

class Team6LearningPlayer(Player):
    def __init__(self, strategy: dict, name="Team6LearningAI"):
        super().__init__(PlayerType.AI, name)
        self.building_priorities = strategy["building_priorities"]
        self.resource_values = strategy["resource_values"]
        self.dev_card_priorities = strategy["dev_card_priorities"]
        self.dice_probabilities = {
            2: 1, 3: 2, 4: 3, 5: 4,
            6: 5, 8: 5, 9: 4, 10: 3,
            11: 2, 12: 1,
        }

    def handle_request(self, message_type: MessageType, possible_actions: list[Action]) -> Action:
        
        """""
        called when the game expects a move.
        currently random valid move from the list of possible actions
        """""
        # TODO: Replace this with logic based on self.current_strategy
        chosen_action = random.choice(possible_actions)
        return chosen_action

    def update_game_state(self, message_type: MessageType, action: Action | GameState):
        """
        Receives updates from the game
        This method can be used to observe the outcome of the last move.
        """
        super().update_game_state(message_type, action)

        # TODO: At game end, update strategy stats
