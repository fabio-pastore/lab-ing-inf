from player.Player import Player
from ui.GameInterface import GameInterface
from random import randint

class CpuPlayer(Player):

    CPU_PLAYER_NAME = "CPU"

    def __init__(self):
        super().__init__(self.CPU_PLAYER_NAME)
        self.next_guess = None

    def reset(self):
        self.next_guess = None

    def guess(self) -> int:
        """
        This function implements a simple guess logic for CPU players.

        If no previous guess was made, a random guess between (MIN_NUMBER, MAX_NUMBER) is made. Else, self.next_guess will contain the value of the next guess.

        Args:
            --

        Returns:
            This function returns an integer containing the value of the CPU players' guess. 
        """
        if self.next_guess is None:
            guess = randint(GameInterface.MIN_NUMBER, GameInterface.MAX_NUMBER)
        else:
            guess = self.next_guess

        return guess
    
    def update_guess(self, prev_guess: int, was_prev_guess_low: bool) -> None:
        if was_prev_guess_low:
            self.next_guess = prev_guess + 1
        else:
            self.next_guess = prev_guess - 1


