from ui.BaseUI import BaseUI
from ui.AsciiUI import AsciiUI
from ui.UnicodeUI import UnicodeUI
from board.Board import Board
from player.HumanPlayer import HumanPlayer
from player.CpuPlayer import CpuPlayer
from player.CpuPlayerGood import CpuPlayerGood
from game_engine.GameEngine import GameEngine

if __name__ == "__main__":

    b: Board = Board()
    ui: BaseUI = UnicodeUI(b)
    hp_1: HumanPlayer = HumanPlayer("Fabio")
    hp_2: HumanPlayer = HumanPlayer("Leonardo")
    cpu_1: CpuPlayer = CpuPlayer()
    cpu_2: CpuPlayer = CpuPlayerGood()
    ge: GameEngine = GameEngine(cpu_2, hp_1, b, ui)
    ge.start_game()

    print("Exiting process with status code (0)")
    exit(0)