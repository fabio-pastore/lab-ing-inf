from ui.GameInterface import GameInterface
from player.HumanPlayer import HumanPlayer
from player.FastCpuPlayer import FastCpuPlayer
from player.CpuPlayer import CpuPlayer

if __name__ == '__main__':

    p1 = FastCpuPlayer()
    p2 = HumanPlayer("Fabio")
    p3 = HumanPlayer("Paolo")
    p4 = CpuPlayer()
    gi = GameInterface([p1, p4])
    gi.start_game()

    exit(0)