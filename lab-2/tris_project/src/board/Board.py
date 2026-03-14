import copy

class Board():

    NUM_BOARD_RC: int = 3
    NO_VAL: int = 0 
    PLAYER_ONE_VAL: int = 1
    PLAYER_TWO_VAL: int = 2

    def __init__(self):
        self.__board_data: list[list[int]] = [[Board.NO_VAL for i in range(Board.NUM_BOARD_RC)] for j in range(Board.NUM_BOARD_RC)]

    def write_value(self, row: int, col: int, player: int) -> None:
        """
        Writes a player's marker to a specific cell on the board.

        Args:
            row (int): The row index of the target cell.
            col (int): The column index of the target cell.
            value (int): The value to write (e.g., Board.PLAYER_ONE_VAL).

        Returns:
            None.
        """
        if row < Board.NUM_BOARD_RC and col < Board.NUM_BOARD_RC and row > -1 and col > -1:
            self.__board_data[row][col] = player
        else:
            raise Exception("[BOARD]: invalid row and/or column values!")

    def get_value(self, row: int, col: int) -> int:
        """
        Retrieves the marker value at a specific coordinate on the board.

        Args:
            row (int): The row index of the target cell.
            col (int): The column index of the target cell.

        Returns:
            int: The value currently stored in the specified cell 
                 (e.g., Board.PLAYER_ONE_VAL, Board.PLAYER_TWO_VAL, or Board.NO_VAL).
        """
        if row < Board.NUM_BOARD_RC and col < Board.NUM_BOARD_RC and row > -1 and col > -1:
            return self.__board_data[row][col]
        else:
            raise Exception("[BOARD]: invalid row and/or column values!")

    def is_written(self, row: int, col: int) -> bool:
        """
        Checks whether a specific cell on the board is already occupied.

        Args:
            row (int): The row index of the target cell.
            col (int): The column index of the target cell.

        Returns:
            bool: True if the cell contains a player's marker, False if it 
                  is empty (i.e., contains Board.NO_VAL).
        """
        return (self.get_value(row, col) != Board.NO_VAL)

    def check_win(self) -> int:
        """
        Evaluates the board to determine if a player has achieved a winning condition.

        Scans all rows, columns, and diagonals to check if any player has 
        successfully placed three of their markers in a continuous line.

        Returns:
            int: The ID of the winning player (e.g., 1 or 2). Returns -1 if no player has won yet.
        """
        # NOTE: these checks are only valid for a 3x3 board! (Board.NUM_BOARD_RC = 3)
        # check rows
        if self.__board_data[0][0] == self.__board_data[0][1] == self.__board_data[0][2] != Board.NO_VAL:
            return self.__board_data[0][0]
        if self.__board_data[1][0] == self.__board_data[1][1] == self.__board_data[1][2] != Board.NO_VAL:
            return self.__board_data[1][0]
        if self.__board_data[2][0] == self.__board_data[2][1] == self.__board_data[2][2] != Board.NO_VAL:
            return self.__board_data[2][0]
        # check cols 
        if self.__board_data[0][0] == self.__board_data[1][0] == self.__board_data[2][0] != Board.NO_VAL:
            return self.__board_data[0][0]
        if self.__board_data[0][1] == self.__board_data[1][1] == self.__board_data[2][1] != Board.NO_VAL:
            return self.__board_data[0][1]
        if self.__board_data[0][2] == self.__board_data[1][2] == self.__board_data[2][2] != Board.NO_VAL:
            return self.__board_data[0][2]
        
        # check diagonals
        if self.__board_data[0][0] == self.__board_data[1][1] == self.__board_data[2][2] != Board.NO_VAL:
            return self.__board_data[0][0]
        if self.__board_data[2][0] == self.__board_data[1][1] == self.__board_data[0][2] != Board.NO_VAL:
            return self.__board_data[2][0]
        
        return -1 # no player has won yet
        
    def is_full(self) -> bool:
        """
        Checks if all cells on the board are currently occupied.

        This method is typically used by the GameEngine to determine if the 
        match has ended in a draw (tie) after verifying that nobody has won.

        Returns:
            bool: True if the board contains no empty cells, False otherwise.
        """
        for i in range(Board.NUM_BOARD_RC):
            for j in range(Board.NUM_BOARD_RC):
                if self.__board_data[i][j] == Board.NO_VAL:
                    return False
        return True

    def reset(self) -> None:
        """
        Resets the board to its initial empty state.

        Iterates through the entire grid and sets every cell back to the 
        default empty value (Board.NO_VAL), effectively clearing all player 
        markers and preparing the board for a new game.

        Args:
            None.

        Returns:
            None.
        """
        for i in range(Board.NUM_BOARD_RC):
            for j in range(Board.NUM_BOARD_RC):
                self.__board_data[i][j] = Board.NO_VAL

    def get_board_data(self) -> list[list[int]]:
        """
        Retrieves a deep copy of the current board state.

        This method ensures that the internal state of the board cannot be
        modified externally.

        Args:
            None.

        Returns:
            list[list[int]]: A matrix representing the current state of the board.
        """
        return copy.deepcopy(self.__board_data) # to avoid external access of the private field 