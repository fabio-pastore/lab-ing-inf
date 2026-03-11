from player.Player import Player
from ui.GameInterface import GameInterface

class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def reset(self):
        pass

    def guess(self) -> int:
        """
        This function implements the guess functionality for human players. 

        Args:
            --

        Returns:
            This function returns an integer with the guess input by the user.
        """
        print(self.name + ", it's your turn! What is your guess?")
        ok_input = False
        while not ok_input:
            try:
                user_guess = int(input(("$ num-guesser ")))
                if (user_guess < GameInterface.MIN_NUMBER or user_guess > GameInterface.MAX_NUMBER):
                    print("Invalid input. Please try again.")
                    continue
                ok_input = True
            except ValueError:
                print("Invalid input. Please try again.")

        return user_guess
    
    def update_guess(self, prev_guess: int, was_prev_guess_low: bool) -> None:
        if was_prev_guess_low:
            print("Too low!")
        else:
            print("Too high!")