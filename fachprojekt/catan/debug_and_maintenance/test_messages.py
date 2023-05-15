import cProfile
from tqdm.contrib.concurrent import process_map

from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.ui.ui_player import UIPlayer
from ai_games.learn_settlers.game.player.player import Player
from ai_games.learn_settlers.ui.display import Display
from ai_games.learn_settlers.utils.message_tester import MessageTester

def main(id:int):
    message_tester = MessageTester(id, 5,4)
    message_tester.run_test()

def run():
    for i in range(10000):
        main(i)
        print(f"Game {i} done")

if __name__ == "__main__":
    cProfile.run("run()", sort="cumtime")
    # run()
    no_games = 1000
    # process_map(main, range(no_games), max_workers=12, chunksize = max(1,no_games//1000))