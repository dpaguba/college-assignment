#! /bin/python3

from ai_games.learn_settlers.client.ls_client import LSClient
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.game.player.player import PlayerType

ADDRESS = "ws://127.0.0.1:8765"

def main():
    print("Starting Client")

    client = LSClient(RandomPlayer("My AI Player"))
    client.connect(ADDRESS)
    client.join_game(0)
    client.start_game()
    # while True:
    #     pass
    client.close_when_finished()

if __name__ == "__main__":
    main()