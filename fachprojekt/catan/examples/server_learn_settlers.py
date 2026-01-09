#! /home/lang1/teaching/Fachprojekt/Carcassonne/.env/bin/python3


from ai_games.learn_settlers.server.lobby import Lobby
from ai_games.learn_settlers.server.matchmaker.match_selection import MatchSelection
from ai_games.learn_settlers.server.matchmaker.turnament import Turnament


def main():
    print("creating carcassonne server")
    matchmaker = Turnament(100,True, 2) # makes 10 Games in each permutation with up to 100 in parallel Logs will be written
    # matchmaker = MatchSelection(10, False)
    lobby = Lobby("127.0.0.1", 8765, matchmaker)
    print("starting server")
    lobby.start_server()
    input("Press Enter to stop server")

if __name__ == '__main__':
    main()