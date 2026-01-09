#! /bin/python3

import uuid
from ai_games.learn_settlers.client.ls_client import LSClient
from ai_games.learn_settlers.game.player.player import PlayerType
from ai_games.learn_settlers.ui.ui_player import UIPlayer

ADDRESS = "ws://127.0.0.1:8765"

def main():
    print("Starting Client")

    player = UIPlayer("AI Player")
    client = LSClient(player)
    client.connect(ADDRESS)
    client.join_game(0)
    assert isinstance(client.player, UIPlayer)
    client.player.start_ui()
    client.close_when_finished()

if __name__ == "__main__":
    main()