from ui.GameInterface import GameInterface
from player.HumanPlayer import HumanPlayer
from player.FastCpuPlayer import FastCpuPlayer

NUM_ITERATIONS = 1000

if __name__ == '__main__':

    p1 = FastCpuPlayer()
    gi = GameInterface([p1])
    gi.start_game(debug=True, iterations=NUM_ITERATIONS)

    exit(0)