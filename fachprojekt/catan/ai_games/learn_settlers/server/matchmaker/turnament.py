import threading
from concurrent.futures import wait, ALL_COMPLETED, as_completed
import time, pandas as pd
from tqdm.auto import tqdm
from typing import Iterable
from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.network_player import NetworkPlayer
from ai_games.learn_settlers.game.player.player import Player
from ai_games.learn_settlers.server.matchmaker.matchmaker import Matchmaker
from ai_games.learn_settlers.com import *
from queue import Queue
import itertools as it

class Turnament(Matchmaker):
    def __init__(self, max_threads, log_results = True, reps = 1):
        super().__init__(max_threads,log_results)
        self.player_queues:dict[str, Queue] = {}
        self.running = threading.Lock()
        self.reps = reps

    def _start_game(self,match_id:int, playerlist: Iterable[str]):
        self.lock.acquire()
        players:list[Player] = [self.player_queues[player].get() for player in playerlist]
        game = LearnSettlers(len(self.games), 5, logging_enabled=self.log_results)
        self.games.append(game)
        self.lock.release()
        for player in players:
            game.add_player(player)
        result = game.run()
        for player in players:
            self.player_queues[player.player_name].put(player)
        # print(f"Game {match_id} finished {time.strftime('%H:%M:%S')}")
        return {p.player_name:r for p,r in zip(players, result)}

    def run(self, playerlist, match_playerlist):
        results = []
        with tqdm(total=len(match_playerlist)) as pbar:
            futures = { self.get_executor().submit(self._start_game, match_id, players) for match_id, players in enumerate(match_playerlist)}
            for future in as_completed(futures):
                results.append(future.result())
                pbar.update(1)
        df = pd.DataFrame(results)
        print("Games finished")
        print(df.mean(axis=0))
        for player_name in playerlist:
            while not self.player_queues[player_name].empty():
                player = self.player_queues[player_name].get_nowait()
                close_msg = MyMessage()
                close_msg.close.client_id = player.client_id
                player.msg_to_client(close_msg)
        self.running.release()

    def start_game(self, match_id: int):
        self.lock.acquire()
        try:
            self.running.acquire(False)
            playerlist = list(self.player_queues.keys())
            match_playerlist = list(it.permutations(playerlist, 4)) * self.reps
            self.get_executor().submit(self.run, playerlist, match_playerlist)
            self.lock.release()
            print(f"Playerlist: {playerlist}")
            print(f"{len(match_playerlist)} Games started")
        except:
            print("Turnament already running")
            pass


    def player_join(self, player: NetworkPlayer, match_id:int|None):
        player_queue = self.player_queues.setdefault(player.player_name, Queue())
        player_queue.put(player)
        joined = MyMessage()
        joined.join.game_id = 0
        joined.join.client_id = player.client_id
        joined.join.player_type = player.player_type
        player.msg_to_client(joined)
        return