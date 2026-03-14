from player.Player import Player
from board.Board import Board
from random import randint

class CpuPlayer(Player):

    CPU_NAME: str = "CPU"
    UNIQUE_CPU_ID: int = 0

    def __init__(self):
        super().__init__(CpuPlayer.CPU_NAME + "@" + str(CpuPlayer.UNIQUE_CPU_ID))
        CpuPlayer.increase_id_counter()

    @classmethod
    def increase_id_counter(cls) -> None:
        cls.UNIQUE_CPU_ID += 1

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
        print("[GameEngine] " + self.name + "'s turn...")
        rand_row: int = None
        rand_col: int = None

        while (rand_row is None or rand_col is None or game_board.is_written(rand_row, rand_col)):
            rand_row = randint(0, Board.NUM_BOARD_RC - 1)
            rand_col = randint(0, Board.NUM_BOARD_RC - 1)

        game_board.write_value(rand_row, rand_col, player_id)
            

    