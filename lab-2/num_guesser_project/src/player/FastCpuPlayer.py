from player.CpuPlayer import CpuPlayer
from ui.GameInterface import GameInterface
from random import randint

class FastCpuPlayer(CpuPlayer):
    def __init__(self):
        super().__init__()
        self.top = GameInterface.MAX_NUMBER
        self.bot = GameInterface.MIN_NUMBER

    def reset(self):
        self.top = GameInterface.MAX_NUMBER
        self.bot = GameInterface.MIN_NUMBER
        super().reset()

    def guess(self) -> int:
        """
        This function implements an optimized binary search logic for the CPU player.

        If no previous guess was made (self.next_guess is None), an integer at the half mark between MIN_NUMBER and MAX_NUMBER is chosen as the starting point. 

        For subsequent turns, the search space is halved based on whether the previous guess was too high or too low, updating self.bot and self.top accordingly, see update_guess().
        The next guess is then calculated as the midpoint of the new range as follows: self.next_guess = self.bot + (self.top - self.bot) // 2

        Args:
            --

        Returns:
            This function returns an integer containing the value of the CPU players' guess.
        """
        if self.next_guess is None:
            guess = (GameInterface.MAX_NUMBER - GameInterface.MIN_NUMBER) // 2
        else:
            guess = self.next_guess

        return guess
    
    def update_guess(self, prev_guess: int, was_prev_guess_low: bool) -> None:
        if was_prev_guess_low:
            self.bot = prev_guess + 1
        else:
            self.top = prev_guess - 1

        self.next_guess = self.bot + (self.top - self.bot) // 2
        

        
