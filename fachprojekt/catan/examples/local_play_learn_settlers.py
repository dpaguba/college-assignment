import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import cProfile, uuid
import concurrent.futures
from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.ui.ui_player import UIPlayer
from ai_games.learn_settlers.game.player.player import Player
from ai_games.learn_settlers.ui.display import Display
from ai_games.learn_settlers.ai.team6.team6_player import Team6Player



def main():
    pool = concurrent.futures.ThreadPoolExecutor(2)
    game = LearnSettlers(0,5)
    player = UIPlayer("MyLocalPlayer", substitute_player=Team6Player("Team6"), autoplay=False)
    game.add_player(player)
    players = [RandomPlayer(f"Player{i}") for i in range(3)]
    for p in players:
        game.add_player(p)
    pool.submit(game.run)
    player.start_ui()


if __name__ == "__main__":
    # cProfile.run("main()", sort="cumtime")
    main()