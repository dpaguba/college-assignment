import cProfile, uuid
from tqdm.auto import tqdm
from tqdm.contrib.concurrent import process_map
from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.ui.ui_player import UIPlayer
from ai_games.learn_settlers.game.player.player import Player
from ai_games.learn_settlers.ui.display import Display

def main(id:int):
    game = LearnSettlers(id,5)
    players = []
    players.append(RandomPlayer( f"player0"))
    players.append(RandomPlayer( f"player1"))
    players.append(RandomPlayer( f"player2"))
    players.append(RandomPlayer( f"player3"))
    for p in players:
        game.add_player(p)
    game.run()

def profile():
    for i in range(1000):
        main(i)
        print(f"Game {i} done")

if __name__ == "__main__":
    cProfile.run("profile()", sort="cumtime")
    # no_games = 1000
    # process_map(main, range(no_games), max_workers=12, chunksize = max(1,no_games//1000))
    
    # start: 100 Games 16.341 s