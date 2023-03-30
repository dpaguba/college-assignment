from ai_games.learn_settlers.game.logic.game_logic import GameLogic
from ai_games.learn_settlers.game.objects.game_state import GameState

from ai_games.learn_settlers.utils.game_log import LOG_VERSION as LOG_VERSION

from ai_games.learn_settlers.utils.game_log import INT_SIZE as INT_SIZE

import gzip, time, uuid

from ai_games.learn_settlers.com import *
from ai_games.learn_settlers.com.message_decoder import MessageDecoder
from ai_games.learn_settlers.game.objects.actions.action import Action

class LogReader():
    def __init__(self, logfile:str) -> None:
        self.logfile = logfile
        stats, self.log = self.read_log(logfile)
        self.res = {p.player_name:r for p,r in zip(self.log[0].game_state.players,self.log[-1].action.phase_action.vp_update)}
        r_vec = list(self.res.values())
        if not  all([r>=0 for r in r_vec]):
            a_gs = self.generate_action_gs_tuples()
            print("error")
        if not max(r_vec) >= 10:
            a_gs = self.generate_action_gs_tuples()
            print("error")
        self.time = stats.create_game.time
        self.game_id = stats.create_game.game_id

    @classmethod
    def read_log(cls, logfile: str) -> tuple[MyMessage,list[MyMessage]]:
        log = []
        compressed = logfile.endswith(".gz")
        if compressed:
            f = gzip.open(logfile, "rb")
        else:
            f = open(logfile, "rb")
        version = int.from_bytes(f.read(1), "big")
        size = int.from_bytes(f.read(INT_SIZE), "big")
        stats = MyMessage()
        stats.ParseFromString(f.read(size))
        assert version == LOG_VERSION
        while True:
            size = int.from_bytes(f.read(INT_SIZE), "big")
            if size == 0:
                break
            l = f.read(size)
            m = MyMessage()
            m.ParseFromString(l)
            log.append(m)
        f.close()
        return stats, log
    
    def generate_game_states(self)-> list[GameState]:
        game_states = []
        game_state = None
        for message in self.log:
            game_state = MessageDecoder.apply_message(message, game_state)
            game_states.append(game_state)
        return game_states
    
    def generate_action_gs_tuples(self) -> list[tuple[Action, GameState]]:
        action_gs = []
        game_state = None
        for i in range(0,len(self.log)):
            message_type, action = MessageDecoder.decode(self.log[i])
            if message_type == MessageType.GAMESTATE:
                assert isinstance(action, GameState)
                game_state = action
                action_gs.append((None, action))
                continue
            assert isinstance(action, Action)
            assert game_state is not None
            game_state = GameLogic.sim_apply_action( game_state, action)
            action_gs.append((action,game_state))
        return action_gs

    def generate_game_states_per_turn(self, game_states:list[GameState]|None = None) -> list[list[GameState]]:
        game_states = game_states if game_states is not None else self.generate_game_states()
        overall_states = []
        turn_states = []
        overall_states.append(turn_states)
        current_turn = game_states[0].turn
        for gs in game_states:
            if gs.turn != current_turn:
                turn_states = []
                overall_states.append(turn_states)
                current_turn = gs.turn
            turn_states.append(gs)
        return overall_states
        
    