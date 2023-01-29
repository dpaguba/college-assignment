#! /bin/python3
import concurrent.futures, time

from ai_games.learn_settlers.client.ls_client import LSClient
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.game.player.player import PlayerType

ADDRESS = "ws://127.0.0.1:8765"

def start_client(name:str):
    client = LSClient(RandomPlayer(name))
    client.connect(ADDRESS)
    client.join_game(-1)
    client.close_when_finished()
    return True

def main():
    print("Starting Clients")
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=72)
    players = [f"random{i}" for i in range(4)] * 12
    futures = [executor.submit(start_client, player) for player in players]
    # time.sleep(5)
    # manager = LSClient(LocalPlayer(f"Manager"))
    # manager.connect(ADDRESS)
    # manager.start_game(0)
    # manager.close()
    concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)

if __name__ == "__main__":
    main()
