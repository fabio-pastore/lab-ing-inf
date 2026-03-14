from board.Board import Board
from player.Player import Player
from ui.BaseUI import BaseUI
from random import randint
from time import sleep

class GameEngine():

    WAIT_INTERVAL_SECONDS: float = 0.75

    def __init__(self, p1: Player, p2: Player, gb: Board, ui: BaseUI):
        if (p1 is p2):
            raise Exception("[GameEngine] Player one and player two must be different!")
        self.player_one: int = p1
        self.player_two: int = p2
        self.board: Board = gb
        self.ui: BaseUI = ui

    def start_game(self) -> None:
        """
        Starts and manages the main game loop.

        This method orchestrates the flow of the game, alternating turns between 
        the two players, triggering the UI to update the board visualization, 
        and checking for win or draw conditions after every move until the 
        match concludes.

        Args:
            None.

        Returns:
            None.
        """ 
        print("[GameEngine] Welcome to TRIS v-1.0 by Fabio!")
        print()

        while True:

            player_one_id: int = None
            player_two_id: int = None
            is_first_move: bool = True

            rval: bool = bool(randint(0, 1)) # choose player ID's uniformly at random (to randomize player symbols)
            if rval:
                player_one_id = Board.PLAYER_ONE_VAL
                player_two_id = Board.PLAYER_TWO_VAL
            else:
                player_one_id = Board.PLAYER_TWO_VAL
                player_two_id = Board.PLAYER_ONE_VAL

            while True:

                if self.board.is_full():
                    print("[GameEngine] Match ended in a draw.")
                    break

                if is_first_move:
                    self.ui.display_board() # display empty board
                    is_first_move = False
                
                self.player_one.make_move(self.board, player_one_id)
                self.ui.display_board()

                ret: int = self.board.check_win()
                if (ret != -1):
                    if (player_one_id == ret):
                        print("[GameEngine] " + self.player_one.name + " has won!")
                    else:
                        print("[GameEngine] " + self.player_two.name + " has won!")
                    break

                if self.board.is_full():
                    print("[GameEngine] Match ended in a draw.")
                    break

                sleep(GameEngine.WAIT_INTERVAL_SECONDS)
                self.player_two.make_move(self.board, player_two_id)
                self.ui.display_board()
                
                ret = self.board.check_win()
                if (ret != -1):
                    if (player_one_id == ret):
                        print("[GameEngine] " + self.player_one.name + " has won!")
                    else:
                        print("[GameEngine] " + self.player_two.name + " has won!")
                    break

                sleep(GameEngine.WAIT_INTERVAL_SECONDS)
 
            input_ok: bool = False
            u_choice: str = ""

            while not input_ok:
                print("[GameEngine] Do you want to play again? Y/N")
                u_choice = input("$ tris >> ").lower()
                if (u_choice == 'y' or u_choice == 'n'):
                    input_ok = True
                else:
                    print("[GameEngine] Invalid input. Please try again.")

            if u_choice == 'y':
                self.board.reset()
                print("[GameEngine] Starting new match...")
                print()
                continue

            else:
                print("[GameEngine] Shutting down...")
                break
            