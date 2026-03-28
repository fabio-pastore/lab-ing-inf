from player.Player import Player
from ui.GameInterface import GameInterface
from random import randint

class CpuPlayer(Player):

    CPU_PLAYER_NAME = "CPU"
    __CPU_ID = 0

    def __init__(self):
        super().__init__(f"{self.CPU_PLAYER_NAME}{CpuPlayer.__CPU_ID}")
        CpuPlayer.__increment_cpu_id()
        self.next_guess = None

    @classmethod
    def __increment_cpu_id(cls):
        cls.__CPU_ID = cls.__CPU_ID + 1

    def reset(self):
        self.next_guess = None

    def update_bounds(self, lower_bound: int, upper_bound: int) -> None:
        pass

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


