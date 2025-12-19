from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.network_player import NetworkPlayer
from ai_games.learn_settlers.game.player.player import Player
from ai_games.learn_settlers.server.matchmaker.matchmaker import Matchmaker
from ai_games.learn_settlers.com import *

class MatchSelection(Matchmaker):
    def __init__(self, max_threads, log_results = False):
        super().__init__(max_threads,log_results)

    def _start_game(self, match: LearnSettlers):
        match.run()
        for player in match.players:
            assert isinstance(player, NetworkPlayer)
            close_msg = MyMessage()
            close_msg.close.client_id = player.client_id
            player.msg_to_client(close_msg)

    def start_game(self, match_id: int):
        match = self.games[match_id]
        self.lock.acquire()
        if match.is_started():
            self.lock.release()
            return
        self.get_executor().submit(self._start_game, match)
        self.lock.release()

    def player_join(self, player: NetworkPlayer, match_id:int|None):
        self.lock.acquire()
        if match_id is not None and match_id >= 0 :
            try:
                match = self.games[match_id]
            except IndexError:
                error_msg = MyMessage()
                error_msg.error.message = "Game not found"
                player.msg_to_client(error_msg)
                return
        else:
            match = self.create_game()
        if match.is_started():
            error_msg = MyMessage()
            error_msg.error.message = "Game already started"
            player.msg_to_client(error_msg)
            return
        match.add_player(player)
        player.set_game_state(match.game_state)

        joined = MyMessage()
        joined.join.game_id = match.game_id
        joined.join.client_id = player.client_id
        joined.join.player_type = player.player_type
        player.msg_to_client(joined)
        self.lock.release()
        return