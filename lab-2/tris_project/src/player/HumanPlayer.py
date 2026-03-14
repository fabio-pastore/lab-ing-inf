from player.Player import Player
from board.Board import Board

class HumanPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def is_valid_input(self, row: int, col: int, gb: Board) -> bool:
        if (row >= 0 and col >= 0 and row < Board.NUM_BOARD_RC and col < Board.NUM_BOARD_RC and not gb.is_written(row, col)):
            return True
        return False

    def make_move(self, game_board: Board, player_id: int) -> None:
        """
        Executes a move for the player during their turn.

        This method determines the coordinates for the player's next move 
        and updates the game board accordingly. For human players, it prompts 
        for standard input; for CPU players, it calculates the move algorithmically.

        Args:
            game_board (Board): The current state of the game board.
            player_id (int): The ID representing the current player.

        Returns:
            None.
        """
        sel_row: int = None
        sel_col: int = None

        while True:
            try:
                print("[GameEngine] " + str(self.name) + ", please enter the row index " + "(0-" + str(Board.NUM_BOARD_RC - 1) + ") " + "of the cell you wish to mark.")
                sel_row = int(input("$ tris >> "))
                print("[GameEngine] Now enter the column index " + "(0-" + str(Board.NUM_BOARD_RC - 1) + ") " + "of the cell you wish to mark.")
                sel_col = int(input("$ tris >> "))
                if (self.is_valid_input(sel_row, sel_col, game_board)):
                    break
                else:
                    print("[ERROR] Cell already written or incorrect coordinates provided. Please try again.")

            except ValueError:
                print("[ERROR] Could not convert user input. Please try again.")

            finally:
                print()

        game_board.write_value(sel_row, sel_col, player_id)

        