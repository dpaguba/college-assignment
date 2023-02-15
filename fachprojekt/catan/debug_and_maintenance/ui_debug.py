import pickle, io, sys
from google.protobuf.any_pb2 import Any
from PySide6.QtWidgets import QApplication, QMainWindow
from ai_games.learn_settlers.ui.board_view import BoardView
from ai_games.learn_settlers.ui.ui_player import UIPlayer

def test_widget():
    app = QApplication([])
    board_view = BoardView()
    scene = board_view.board_scene
    scene.addText("Test Text")
    board_view.show()
    sys.exit(app.exec())


def main():
    test_widgets = False
    if test_widgets:
        test_widget()
    else:
        player = UIPlayer()
        player.start_ui()


if __name__ == "__main__":
    main()