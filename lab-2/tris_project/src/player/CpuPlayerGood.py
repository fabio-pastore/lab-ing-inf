from player.CpuPlayer import CpuPlayer
from board.Board import Board

class CpuPlayerGood(CpuPlayer):
    def __init__(self):
        super().__init__()

    def _has_two_in_row(self, game_board: Board | list[list[int]], player_id: int) -> tuple[bool, tuple[int, int]]:
        """
        Checks if the specified player has two markers and one empty space in any line.

        This method scans all rows, columns, and diagonals of the board to find an 
        immediate winning opportunity or a critical threat that needs blocking. It 
        supports both a Board object and a raw 2D list (matrix) for simulation purposes.

        Args:
            game_board (Board | list[list[int]]): The current game board or a raw matrix representing it.
            player_id (int): The ID of the player to check for two-in-a-row.

        Returns:
            tuple[bool, tuple[int, int]]: A tuple where the first element is True if a 
                                          two-in-a-row is found, and the second element 
                                          contains the (row, col) coordinates of the empty cell. 
                                          Returns (False, (-1, -1)) if none is found.
        """
        if isinstance(game_board, Board):
            board_data: list[list[int]] = game_board.get_board_data()
        else:
            board_data: list[list[int]] = game_board # in the case we have passed directly the board matrix

        empty: int = Board.NO_VAL
        
        # NOTE: these checks work only on 3x3 grids (Board.NUM_BOARD_RC = 3)
        # --- CHECK ROWS ---
        # row 0
        if board_data[0][0] == board_data[0][1] == player_id and board_data[0][2] == empty: return (True, (0, 2))
        if board_data[0][0] == board_data[0][2] == player_id and board_data[0][1] == empty: return (True, (0, 1))
        if board_data[0][1] == board_data[0][2] == player_id and board_data[0][0] == empty: return (True, (0, 0))
        # row 1
        if board_data[1][0] == board_data[1][1] == player_id and board_data[1][2] == empty: return (True, (1, 2))
        if board_data[1][0] == board_data[1][2] == player_id and board_data[1][1] == empty: return (True, (1, 1))
        if board_data[1][1] == board_data[1][2] == player_id and board_data[1][0] == empty: return (True, (1, 0))
        # row 2
        if board_data[2][0] == board_data[2][1] == player_id and board_data[2][2] == empty: return (True, (2, 2))
        if board_data[2][0] == board_data[2][2] == player_id and board_data[2][1] == empty: return (True, (2, 1))
        if board_data[2][1] == board_data[2][2] == player_id and board_data[2][0] == empty: return (True, (2, 0))

        # --- CHECK COLUMNS ---
        # column 0
        if board_data[0][0] == board_data[1][0] == player_id and board_data[2][0] == empty: return (True, (2, 0))
        if board_data[0][0] == board_data[2][0] == player_id and board_data[1][0] == empty: return (True, (1, 0))
        if board_data[1][0] == board_data[2][0] == player_id and board_data[0][0] == empty: return (True, (0, 0))
        # column 1
        if board_data[0][1] == board_data[1][1] == player_id and board_data[2][1] == empty: return (True, (2, 1))
        if board_data[0][1] == board_data[2][1] == player_id and board_data[1][1] == empty: return (True, (1, 1))
        if board_data[1][1] == board_data[2][1] == player_id and board_data[0][1] == empty: return (True, (0, 1))
        # column 2
        if board_data[0][2] == board_data[1][2] == player_id and board_data[2][2] == empty: return (True, (2, 2))
        if board_data[0][2] == board_data[2][2] == player_id and board_data[1][2] == empty: return (True, (1, 2))
        if board_data[1][2] == board_data[2][2] == player_id and board_data[0][2] == empty: return (True, (0, 2))

        # --- CHECK DIAGONALS ---
        # diagonal 1
        if board_data[0][0] == board_data[1][1] == player_id and board_data[2][2] == empty: return (True, (2, 2))
        if board_data[0][0] == board_data[2][2] == player_id and board_data[1][1] == empty: return (True, (1, 1))
        if board_data[1][1] == board_data[2][2] == player_id and board_data[0][0] == empty: return (True, (0, 0))
        # diagonal 2 
        if board_data[0][2] == board_data[1][1] == player_id and board_data[2][0] == empty: return (True, (2, 0))
        if board_data[0][2] == board_data[2][0] == player_id and board_data[1][1] == empty: return (True, (1, 1))
        if board_data[2][0] == board_data[1][1] == player_id and board_data[0][2] == empty: return (True, (0, 2))

        return (False, (-1, -1))
    
    def _count_winning_opportunities(self, board_data: list[list[int]], player_id: int) -> int:
        """
        Counts the total number of winning opportunities for a specific player.

        A winning opportunity is defined as a line (row, column, or diagonal) that 
        contains exactly two markers of the specified player and one empty cell. 
        This is a helper function primarily used for evaluating forks.

        Args:
            board_data (list[list[int]]): A 2D list representing the board state.
            player_id (int): The ID of the player to evaluate.

        Returns:
            int: The total count of independent winning lines available to the player.
        """
        count: int = 0
        size: int = Board.NUM_BOARD_RC
        empty: int = Board.NO_VAL

        # check rows, columns and diagonals
        lines: list[list[int]] = []
        # R
        for r in range(size): lines.append([board_data[r][0], board_data[r][1], board_data[r][2]])
        # C
        for c in range(size): lines.append([board_data[0][c], board_data[1][c], board_data[2][c]])
        # D
        lines.append([board_data[0][0], board_data[1][1], board_data[2][2]])
        lines.append([board_data[0][2], board_data[1][1], board_data[2][0]])

        for line in lines:
            if line.count(player_id) == 2 and line.count(empty) == 1:
                count += 1
        return count
    
    def _find_fork(self, game_board: Board, player_id: int) -> tuple[int, int] | None:
        """
        Simulates all possible moves to find one that creates a fork.

        A fork is a scenario where a single move creates two unblocked winning 
        opportunities (two-in-a-row lines), guaranteeing a win on the next turn.

        Args:
            game_board (Board): The current state of the game board.
            player_id (int): The ID representing the CPU player.

        Returns:
            tuple[int, int] | None: The (row, col) coordinates of the fork move, 
                                    or None if no such move exists.
        """
        board_data: list[list[int]] = game_board.get_board_data()
        size: int = Board.NUM_BOARD_RC
        
        for r in range(size):
            for c in range(size):
                if board_data[r][c] == Board.NO_VAL:
                    # simulate own move
                    board_data[r][c] = player_id
                    if self._count_winning_opportunities(board_data, player_id) >= 2:
                        board_data[r][c] = Board.NO_VAL 
                        return (r, c)
                    board_data[r][c] = Board.NO_VAL 
        return None
    
    def _get_all_forks(self, game_board: Board, opponent_id: int) -> list[tuple[int, int]]:
        """
        Identifies all possible coordinates where the opponent could create a fork.

        The method simulates placing an opponent's marker in every empty cell and 
        uses _count_winning_opportunities to check if that move results in two or 
        more winning lines. 

        Args:
            game_board (Board): The current state of the game board.
            opponent_id (int): The ID representing the opposing player.

        Returns:
            list[tuple[int, int]]: A list containing the (row, col) coordinates of 
                                   all potential opponent forks.
        """
        forks: list[tuple[int, int]] = []
        board_data: list[list[int]] = game_board.get_board_data()
        size: int = Board.NUM_BOARD_RC
        
        for r in range(size):
            for c in range(size):
                if board_data[r][c] == Board.NO_VAL:
                    board_data[r][c] = opponent_id
                    if self._count_winning_opportunities(board_data, opponent_id) >= 2:
                        forks.append((r, c))
                    board_data[r][c] = Board.NO_VAL
        return forks
    
    def _force_defense_without_fork(self, game_board: Board, player_id: int, opponent_id: int) -> tuple[int, int] | None:
        """
        Finds a safe offensive move to force the opponent into defending.

        When the opponent has multiple potential forks, this method calculates a move 
        that threatens a win (forcing the opponent to block), while ensuring that the 
        required blocking move does not simultaneously allow the opponent to complete 
        one of their forks.

        Args:
            game_board (Board): The current state of the game board.
            player_id (int): The ID representing the CPU player.
            opponent_id (int): The ID representing the opposing player.

        Returns:
            tuple[int, int] | None: The (row, col) coordinates of the safe offensive move, 
                                    or None if no such move is found.
        """
        board_data: list[list[int]] = game_board.get_board_data()
        size: int = Board.NUM_BOARD_RC
        
        for r in range(size):
            for c in range(size):
                if board_data[r][c] == Board.NO_VAL:
                    # simulate own move
                    board_data[r][c] = player_id
                    # check if this move creates two in a row thread
                    retval : tuple[bool, tuple[int, int]] = self._has_two_in_row(board_data, player_id)
                    success: bool = retval[0]
                    threat_coord: tuple[int, int] = retval[1]
                    if success:
                        # check if cell where opponent has to defend does not allow the opponent to create a retaliatory fork
                        board_data[threat_coord[0]][threat_coord[1]] = opponent_id
                        if self._count_winning_opportunities(board_data, opponent_id) < 2:
                            board_data[r][c] = Board.NO_VAL
                            board_data[threat_coord[0]][threat_coord[1]] = Board.NO_VAL
                            return (r, c)
                        board_data[threat_coord[0]][threat_coord[1]] = Board.NO_VAL
                    board_data[r][c] = Board.NO_VAL
        return None

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

        opponent_id: int = None

        if player_id == Board.PLAYER_ONE_VAL:
            opponent_id = Board.PLAYER_TWO_VAL
        else:
            opponent_id = Board.PLAYER_ONE_VAL

        """
        Choose the first available move from the following list:
        - Win: If the player has two in a row, they can place a third to get three in a row.
        - Block: If the opponent has two in a row, the player must play the third themselves to block the opponent.
        - Fork: Cause a scenario where the player has two ways to win (two non-blocked lines of 2).
        - Blocking an opponent's fork: If there is only one possible fork for the opponent, the player should block it. Otherwise, the player should block all forks in any way that simultaneously allows them to make two in a row. Otherwise, the player should make a two in a row to force the opponent into defending, as long as it does not result in them producing a fork. For example, if "X" has two opposite corners and "O" has the center, "O" must not play a corner move to win. (Playing a corner move in this scenario produces a fork for "X" to win.)
        - Center: A player marks the center. (If it is the first move of the game, playing a corner move gives the second player more opportunities to make a mistake and may therefore be the better choice; however, it makes no difference between perfect players.)
        - Opposite corner: If the opponent is in the corner, the player plays the opposite corner.
        - Empty corner: The player plays in a corner square.
        - Empty side: The player plays in a middle square on any of the four sides.
        """

        # 1. WIN: place third after two in a row
        ret_value: tuple[bool, tuple[int, int]] = self._has_two_in_row(game_board, player_id) # check if we have two in a row to potentially win the game
        if (ret_value[0]):
            game_board.write_value(ret_value[1][0], ret_value[1][1], player_id)
            return None
        
        # 2. DEFENSE: block two in a row
        ret_value = self._has_two_in_row(game_board, opponent_id) # check if opponent has two in a row to potentially block the threat
        if (ret_value[0]):
            game_board.write_value(ret_value[1][0], ret_value[1][1], player_id)
            return None
        
        # 3. FORK: create a scenario where the player has two ways to win.
        fork_move: tuple[int, int] | None = self._find_fork(game_board, player_id)
        if fork_move:
            game_board.write_value(fork_move[0], fork_move[1], player_id)
            return None

        # 4. BLOCKING AN OPPONENT'S FORK
        opponent_forks: list[tuple[int, int]] = self._get_all_forks(game_board, opponent_id)
        if len(opponent_forks) == 1:
            # if there is only one possible fork for the opponent, block it.
            game_board.write_value(opponent_forks[0][0], opponent_forks[0][1], player_id)
            return None
        elif len(opponent_forks) > 1:
            # if more than one, force the opponent into defending.
            threat_move: tuple[int, int] | None = self._force_defense_without_fork(game_board, player_id, opponent_id)
            if threat_move:
                game_board.write_value(threat_move[0], threat_move[1], player_id)
                return None

        # 5. CENTER: mark the center if empty.
        if game_board.get_value(1, 1) == Board.NO_VAL:
            game_board.write_value(1, 1, player_id)
            return None

        # 6. OPPOSITE CORNER: if opponent is in a corner, play the opposite corner.
        corners: list[tuple[int, int]] = [(0, 0), (0, 2), (2, 0), (2, 2)]
        opposite_map: dict[tuple[int, int], tuple[int, int]] = {(0, 0): (2, 2), (0, 2): (2, 0), (2, 0): (0, 2), (2, 2): (0, 0)}
        for c in corners:
            if game_board.get_value(c[0], c[1]) == opponent_id:
                opp: tuple[int, int] = opposite_map[c]
                if game_board.get_value(opp[0], opp[1]) == Board.NO_VAL:
                    game_board.write_value(opp[0], opp[1], player_id)
                    return None

        # 7. EMPTY CORNER: play in any available corner.
        for c in corners:
            if game_board.get_value(c[0], c[1]) == Board.NO_VAL:
                game_board.write_value(c[0], c[1], player_id)
                return None

        # 8. EMPTY SIDE: play in any middle square on the four sides.
        sides: list[tuple[int, int]] = [(0, 1), (1, 0), (1, 2), (2, 1)]
        for s in sides:
            if game_board.get_value(s[0], s[1]) == Board.NO_VAL:
                game_board.write_value(s[0], s[1], player_id)
                return None

        return None 


        