import random, numpy as np
from ai_games.learn_settlers.com.message_type import MessageType
from ai_games.learn_settlers.game.logic.discard_helper import DiscardHelper
from ai_games.learn_settlers.game.objects.actions import *
from ai_games.learn_settlers.game.objects.actions.phase_action import GamePhase
from ai_games.learn_settlers.game.objects.game_state import GameState, RobberState
from ai_games.learn_settlers.game.player.player import Player, PlayerType

# Basic Player class that does random moves
class Team3Player(Player):
    def __init__(self, name:str = "") -> None:
        super().__init__(PlayerType.AI, name=name)

    def handle_request(self, message_type: MessageType, possible_actions: list[Action]):
        assert self.game_state is not None
        my_no = self.player_no
        # choose a random action
        # TODO replace with a more clever option 
        my_action = possible_actions[random.randint(0, len(possible_actions)-1)]
        
        # Handle resource discarding
        if isinstance(my_action, DiscardAction):
            discard_logic = DiscardHelper(self.game_state, my_action)
            
            possible_discards = discard_logic.propose_discard()
            my_discard = possible_discards[random.randint(0, len(possible_discards)-1)]
            while discard_logic.apply_discard(my_discard):
                possible_discards = discard_logic.propose_discard()
                my_discard = possible_discards[random.randint(0, len(possible_discards)-1)]
            my_action = discard_logic.get_action()
        
        # check if player to player trade can be done
        if (len(self.game_state.discarding) == 0 and 
            not self.game_state.monopoly and 
            not self.game_state.trade_ongoing and 
            self.game_state.road_building == 0 and 
            self.game_state.year_of_plenty == 0 and 
            self.game_state.robber_state == RobberState.NO_STATE and
            self.game_state.phase == GamePhase.PLAY
            ):
            # try to trade with an other player with a probabliity of 10%
            if random.random() < 0.1:
                max_res = np.max(self.game_state.players[my_no].resources[0:5])
                if max_res <= 0:
                    return my_action
                max_id = np.argwhere(max_res == self.game_state.players[my_no].resources[0:5])[0][0]
                my_res = np.zeros(6,int)
                my_res[[max_id,-1]] = 1
                other_player = random.randint(0,2)
                if other_player == my_no:
                    other_player += 1
                if self.game_state.players[other_player].resources[-1] == 0:
                    return my_action
                possible_res = np.argwhere(self.game_state.players[other_player].resources[0:5] > 0)[0]
                other_res = np.zeros(6,int)
                other_res[[np.random.choice(possible_res),-1]] = 1
                
                my_trade_action = TradeAction(my_no, other_player, my_res, other_res)
                return my_trade_action
            
        return my_action
