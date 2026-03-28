from abc import ABC, abstractmethod
from board.Board import Board

class BaseUI(ABC):

    @abstractmethod
    def __init__(self, board: Board):
        self.board: Board = board

    @abstractmethod
    def display_board() -> None:
        pass
    
    @classmethod
    @abstractmethod
    def display_data(cls, board_data: list[list[int]]) -> None:
        pass
    
    @classmethod
    def _board_val_to_psymbol(cls, val: int) -> str:
        if (val == Board.PLAYER_ONE_VAL):
            return cls.PLAYER_ONE_CHAR
        elif (val == Board.PLAYER_TWO_VAL):
            return cls.PLAYER_TWO_CHAR
        else:
            pass