from ui.BaseUI import BaseUI
from board.Board import Board

class AsciiUI(BaseUI):

    # NOTE: this UI only supports 3x3 boards for the time being.

    ROW_DELIMITER: str = "+---+---+---+"
    PLAYER_ONE_CHAR: str = "X"
    PLAYER_TWO_CHAR: str = "O"

    def __init__(self, board: Board):
        super().__init__(board)

    def display_board(self) -> None:
        """
        Renders the current state of the game board to the terminal.

        This method reads the internal data from the board and prints it 
        using the specific character set (ASCII or Unicode) defined by the 
        concrete UI class, ensuring the logic is decoupled from the graphics.

        Args:
            game_board (Board): The game board object to be displayed.

        Returns:
            None.
        """
        data: list[list[int]] = self.board.get_board_data()
        for i in range(Board.NUM_BOARD_RC):
            print(AsciiUI.ROW_DELIMITER)
            for j in range(Board.NUM_BOARD_RC):
                board_val: int = data[i][j]
                if board_val == Board.NO_VAL:
                    print("|   ", end="")
                else:
                    print("| " + self._board_val_to_psymbol(board_val) + " ", end="") 
            print("|")
        print(AsciiUI.ROW_DELIMITER)


        