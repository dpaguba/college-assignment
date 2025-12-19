from concurrent.futures import ThreadPoolExecutor
import threading
from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.network_player import NetworkPlayer
from abc import ABC, abstractmethod

from ai_games.learn_settlers.com import *

class Matchmaker(ABC):

    def __init__(self, max_threads, log_results = False) -> None:
        # Multithreading
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=max_threads)

        # Game
        self.games:list[LearnSettlers] = []
        self.log_results = log_results

    def get_executor(self):
        return self.executor

    def create_game(self) :
        new_match = LearnSettlers(len(self.games), 5, logging_enabled=self.log_results)
        self.games.append(new_match)
        return new_match

    @abstractmethod
    def start_game(self, match_id:int):
        raise NotImplementedError

    @abstractmethod
    def player_join(self, player:NetworkPlayer, match_id:int|None):
        raise NotImplementedError